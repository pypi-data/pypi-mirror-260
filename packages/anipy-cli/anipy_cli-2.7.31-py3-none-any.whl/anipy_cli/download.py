import re
import urllib
from pathlib import Path

import m3u8
import requests
import shutil
import sys

from tqdm import tqdm
from requests.adapters import HTTPAdapter, Retry
from concurrent.futures import ThreadPoolExecutor
from better_ffmpeg_progress import FfmpegProcess
from moviepy.editor import ffmpeg_tools

from anipy_cli.misc import response_err, error, keyboard_inter
from anipy_cli.colors import colors, color, cprint
from anipy_cli.config import Config


class download:
    """
    Download Class.
    A entry with all fields is required.
    """

    def __init__(
        self, entry, quality, ffmpeg=False, dl_path: Path = None, file_name_format=""
    ) -> None:
        try:
            self.quality = int(quality)
        except ValueError:
            self.quality = quality
        self.is_audio = None
        self.content_audio_media = None
        self._m3u8_content = None
        self.session = None
        self.entry = entry
        self.ffmpeg = ffmpeg
        self.dl_path = dl_path
        self.file_name_format = file_name_format
        if dl_path is None:
            self.dl_path = Config().download_folder_path
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "referer": self.entry.embed_url,
        }

    def download(self):
        show_name = self._get_valid_pathname(self.entry.show_name)
        self.show_folder = self.dl_path / f"{show_name}"

        if Config().download_remove_dub_from_folder_name:
            if show_name.endswith(" (Dub)"):
                self.show_folder = self.dl_path / f"{show_name[:-6]}"
                print(self.show_folder)

        self.dl_path.mkdir(exist_ok=True, parents=True)
        self.show_folder.mkdir(exist_ok=True)
        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update(self.headers)

        fname = self._get_fname()
        dl_path = self.show_folder / fname

        if dl_path.is_file():
            print("-" * 20)
            cprint(
                colors.GREEN,
                "Skipping Already Existing: ",
                colors.RED,
                f"{self.entry.show_name} EP: {self.entry.ep} - {self.entry.quality}",
            )
            return dl_path

        print("-" * 20)
        cprint(
            colors.CYAN,
            "Downloading: ",
            colors.RED,
            f"{self.entry.show_name} EP: {self.entry.ep} - {self.entry.quality}",
        )

        if "m3u8" in self.entry.stream_url:
            cprint(colors.CYAN, "Type: ", colors.RED, "m3u8")
            if self.ffmpeg or Config().ffmpeg_hls:
                cprint(colors.CYAN, "Downloader: ", colors.RED, "ffmpeg")
                self.ffmpeg_dl()
                return dl_path

            cprint(colors.CYAN, "Downloader:", colors.RED, "internal")
            self.multithread_m3u8_dl()
        elif "mp4" in self.entry.stream_url:
            cprint(colors.CYAN, "Type: ", colors.RED, "mp4")
            self.mp4_dl(self.entry.stream_url)

        return dl_path

    def ffmpeg_dl(self):
        Config().user_files_path.mkdir(exist_ok=True, parents=True)
        Config().ffmpeg_log_path.mkdir(exist_ok=True, parents=True)
        fname = self._get_fname()

        dl_path = self.show_folder / fname

        ffmpeg_process = FfmpegProcess(
            [
                "ffmpeg",
                "-headers",
                f"referer:{self.entry.embed_url}",
                "-i",
                self.entry.stream_url,
                "-vcodec",
                "copy",
                "-acodec",
                "copy",
                "-scodec",
                "mov_text",
                "-c",
                "copy",
                str(dl_path),
            ]
        )

        try:
            ffmpeg_process.run(
                ffmpeg_output_file=str(
                    Config().ffmpeg_log_path / fname.replace("mp4", "log")
                )
            )
            cprint(colors.CYAN, "Download finished.")
        except KeyboardInterrupt:
            error("interrupted deleting partially downloaded file")
            fname.unlink()

    def ffmpeg_merge(self, input_file, audio_input_file):
        Config().user_files_path.mkdir(exist_ok=True, parents=True)
        Config().ffmpeg_log_path.mkdir(exist_ok=True, parents=True)
        fname = self._get_fname()

        dl_path = self.show_folder / fname

        merged_video_ts = self.merge_ts_files(input_file)
        merged_audio_ts = None
        if audio_input_file:
            merged_audio_ts = self.merge_ts_files(audio_input_file, "_audio")

        try:
            cprint(colors.CYAN, "Merging Parts using Movie.py...")
            if audio_input_file:
                ffmpeg_tools.ffmpeg_merge_video_audio(
                    merged_video_ts,
                    merged_audio_ts,
                    str(dl_path),
                    vcodec="copy",
                    acodec="copy",
                    ffmpeg_output=False,
                    logger="bar",
                )
            else:
                ffmpeg_tools.ffmpeg_merge_video_audio(
                    merged_video_ts,
                    merged_video_ts,
                    str(dl_path),
                    vcodec="copy",
                    acodec="copy",
                    ffmpeg_output=False,
                    logger="bar",
                )

            cprint(colors.CYAN, "Merge finished.")
        except KeyboardInterrupt:
            error("interrupted deleting partially downloaded file")
            fname.unlink()

    def merge_ts_files(self, input_file, suffix=""):
        filename = f"{self.temp_folder}/{self._get_valid_pathname(self.entry.show_name)}_{self.entry.ep}_merged{suffix}.ts"
        # Parse playlist for filenames with ending .ts and put them into the list ts_filenames
        with open(input_file, "r") as playlist:
            ts_filenames = [
                line.rstrip() + f"{suffix}"
                for line in playlist
                if not line.lstrip().startswith("#")
            ]
        # open one ts_file from the list after another and append them to merged.ts
        with open(filename, "wb") as merged:
            for ts_file in ts_filenames:
                with open(ts_file, "rb") as mergefile:
                    shutil.copyfileobj(mergefile, merged)
        return filename

    def mp4_dl(self, dl_link):
        """

        :param dl_link:
        :type dl_link:
        :return:
        :rtype:
        """
        r = self.session.get(dl_link, headers=self.headers, stream=True)
        response_err(r, dl_link)
        total = int(r.headers.get("content-length", 0))
        fname = self.show_folder / self._get_fname()
        try:
            with fname.open("wb") as out_file, tqdm(
                desc=self.entry.show_name,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in r.iter_content(chunk_size=1024):
                    size = out_file.write(data)
                    bar.update(size)
        except KeyboardInterrupt:
            error("interrupted deleting partially downloaded file")
            fname.unlink()

        cprint(colors.CYAN, "Download finished.")

    def download_ts(self, m3u8_segments, retry=0):
        self.counter += 1
        audio_suffix = ""
        uri = urllib.parse.urljoin(m3u8_segments.base_uri, m3u8_segments.uri)
        if not self._is_url(uri):
            input(f"uri: {uri} is not an uri")
            return

        if self.is_audio:
            audio_suffix = "audio"
        filename = self._get_filename(uri, self.temp_folder, audio_suffix)
        headers = self.headers
        retry_count = 0
        while not Path(filename).is_file() and retry_count < 20:
            cprint(
                colors.CYAN,
                f"Downloading {audio_suffix} Part: {self.counter}/{self.segment_count}",
                end="",
            )
            print("\r", end="")

            try:
                with self.session.get(
                    uri, timeout=10, headers=headers, stream=False
                ) as response:
                    if response.status_code == 416:
                        return

                    response.raise_for_status()

                    with open(filename, "wb") as fout:
                        fout.write(response.content)

            except Exception as e:
                exit(e.__str__())
            retry_count += 1

    def multithread_m3u8_dl(self):
        """
        Multithread download
        function for m3u8 links.
        - Creates show and temp folder
        - Starts ThreadPoolExecutor instance
          and downloads all ts links
        - Merges ts files
        - Deletes temp folder

        :return:
        :rtype:
        """

        self.temp_folder = self.show_folder / f"{self.entry.ep}_temp"
        self.temp_folder.mkdir(exist_ok=True)
        self.counter = 0

        self._m3u8_content = self._download_m3u8(
            self.entry.stream_url, 10, self.headers
        )

        assert self._m3u8_content.is_variant is False

        try:
            if self.content_audio_media and not self.content_audio_media.is_variant:
                self.segment_count = len(self.content_audio_media.segments)
                self.is_audio = True
                with ThreadPoolExecutor(12) as pool_audio:
                    pool_audio.map(self.download_ts, self.content_audio_media.segments)
            self.is_audio = False
            self.counter = 0
            self.segment_count = len(self._m3u8_content.segments)
            print("\n")
            with ThreadPoolExecutor(12) as pool_video:
                pool_video.map(self.download_ts, self._m3u8_content.segments)
        except KeyboardInterrupt:
            shutil.rmtree(self.temp_folder)
            keyboard_inter()
            exit()

        input_file = self._dump_m3u8(self._m3u8_content)
        audio_input_file = None
        if self.content_audio_media and not self.content_audio_media.is_variant:
            self.is_audio = True
            audio_input_file = self._dump_m3u8(self.content_audio_media)

        cprint("\n", colors.CYAN, "Parts Downloaded")
        try:
            self.ffmpeg_merge(input_file, audio_input_file)
        except FileNotFoundError:
            # This restarts the download if a file is missing
            error("Missing a download part, restarting download")
            return self.multithread_m3u8_dl()

        cprint("\n", colors.CYAN, "Parts Merged")
        shutil.rmtree(self.temp_folder)

    def _download_m3u8(self, uri, timeout, headers, is_audio=False):
        if self._is_url(uri):
            resp = self.session.get(uri, timeout=timeout, headers=self.headers)
            resp.raise_for_status()
            raw_content = resp.content.decode(resp.encoding or "utf-8")
            base_uri = urllib.parse.urljoin(uri, ".")
        else:
            with open(uri) as fin:
                raw_content = fin.read()
                base_uri = Path(uri)
        content = m3u8.M3U8(raw_content, base_uri=base_uri)
        if content.is_variant:
            if self.content_audio_media is not None:
                content.add_media(media=self.content_audio_media)

            # sort
            content.playlists.sort(key=lambda x: x.stream_info.bandwidth, reverse=True)

            selected_index = 0
            if self.quality == "worst":
                selected_index = len(content.playlists) - 1

            for index, playlist in enumerate(content.playlists):
                cprint(
                    colors.GREEN,
                    "Playlist Index: ",
                    colors.RED,
                    index,
                    "\n",
                    colors.GREEN,
                    "Resolution at this index: ",
                    colors.RED,
                    playlist.stream_info.resolution,
                    "\n\n",
                )

                if self.quality in playlist.stream_info.resolution:
                    selected_index = index

            try:
                for media in content.media:
                    if content.playlists[selected_index].stream_info.audio in str(
                        media
                    ):
                        self.content_audio_media = media

                chosen_uri = content.playlists[selected_index].uri
                if not self._is_url(chosen_uri):
                    chosen_uri = urllib.parse.urljoin(content.base_uri, chosen_uri)
                if self.content_audio_media is not None:
                    media_uri = self.content_audio_media.uri
                    self.content_audio_media = self._download_m3u8(
                        media_uri, timeout, headers, True
                    )
                cprint(
                    colors.GREEN,
                    "Quality for Download:",
                    colors.YELLOW,
                    content.playlists[selected_index].stream_info.resolution,
                )
                return self._download_m3u8(chosen_uri, timeout, headers)

            except (ValueError, IndexError):
                exit("Failed to get stream for chosen quality")

        else:
            self._download_key(content)

        return content

    def _dump_m3u8(self, content):
        audio_suffix = ""
        for index, segment in enumerate(content.segments):
            content.segments[index].uri = self._get_filename(
                segment.uri, self.temp_folder
            )

        if self.is_audio:
            audio_suffix = "_audio"
        filename = self._get_filename(f"master{audio_suffix}.m3u8", self.temp_folder)
        content.dump(filename)
        return filename

    def _download_key(self, content):
        for key in content.keys:
            if key:
                uri = key.absolute_uri
                filename = self._get_filename(uri, self.temp_folder)

                with self.session.get(
                    uri, timeout=10, headers=self.headers
                ) as response:
                    response.raise_for_status()
                    with open(filename, "wb") as fout:
                        fout.write(response.content)

                key.uri = filename.__str__().replace(
                    "\\", "/"
                )  # ffmpeg error when using \\ in windows

    def _get_fname(self) -> str:
        """
        This function returns what the filename for the outputted video should be.

        It finds this by using data in self.entry and the Config.

        Returns a string which should be the filename.
        """

        show_name = self._get_valid_pathname(self.entry.show_name)

        file_format = (
            self.file_name_format
            if self.file_name_format
            else Config().download_name_format
        )

        return file_format.format(
            show_name=show_name,
            episode_number=self.entry.ep,
            quality=self.entry.quality,
        )

    @staticmethod
    def _get_valid_pathname(name: str):
        WIN_INVALID_CHARS = ["\\", "/", ":", "*", "?", "<", ">", "|", '"']

        if sys.platform == "win32":
            name = "".join(["" if x in WIN_INVALID_CHARS else x for x in name])

        name = "".join(
            [i for i in name if i.isascii()]
        )  # Verify all chars are ascii (eject if not)
        name = "-".join(name.split())  # Clean all white spaces, including tabs and such

        return name

    @staticmethod
    def _is_url(uri):
        return re.match(r"https?://", uri) is not None

    @staticmethod
    def _get_filename(uri, directory, suffix=""):
        if suffix:
            suffix = f"_{suffix}"
        basename = urllib.parse.urlparse(uri).path.split("/")[-1]
        filename = Path("{}/{}{}".format(directory, basename, suffix)).__str__()
        return filename
