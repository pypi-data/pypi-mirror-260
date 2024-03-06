# ffpe.py
# -------------

import os
import gc
import re
import time
import subprocess
import logging
from tqdm import tqdm
import numpy as np
from typing import Optional, List
from functools import lru_cache
from rich.box import ROUNDED
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

console = Console()


def clear_console():
    # CLEAR CONSOLE SCREEN.
    """
    >>> CLEAR SCREEN FUNCTION.
    """
    if os.name == "nt":
        _ = os.system("cls")  # FOR WINDOWS
    else:
        _ = os.system("clear")  # FOR LINUX/MACOS


class ffpe:
    """
    >>> FFPE - SIMPLE WRAPPER FOR FFPE.

    >>> THIS CLASS PROVIDES CONVENIENT INTERFACE FOR USING FFPE TO CONVERT MULTIMEDIA FILES.

    ⇨ ATTRIBUTE'S
    --------------
    >>> FFpe_PATH : STR
        >>> PATH TO THE FFPE EXECUTABLE.
    >>> LOGGER : LOGGING.LOGGER
        >>> LOGGER INSTANCE FOR LOGGING MESSAGES.

    ⇨ METHOD'S
    -----------
    >>> CONVERT(INPUT_FILES, OUTPUT_DIR, CV=NONE, CA=NONE, S=NONE, HWACCEL=NONE,
    >>>         AR=NONE, AC=NONE, BA=NONE, R=NONE, F=NONE, PRESET=NONE, BV=NONE)
    >>>     CONVERT MULTIMEDIA FILES USING FFMPEG.

    ⇨ CONVERT( )
    -------------
        >>> NOTE: USE "convert()" TO CONVERT MEDIA FILES.

        >>> EXAMPLE:


        ```python
         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         # INSTANTIATE THE FFPE CLASS

         from MediaSwift import *
         ffpe_instance = ffpe()

         # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        ... input_files = [r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE']       # input_files [MULTIPLE CONVERT]
        ... input_files = [r'PATH_TO_INPUT_FILE']                              # input_files [SINGLE CONVERT]

         output_dir = r'OUTPUT_FOLDER'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG.
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba='192k',        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             bv='50m',         # VIDEO BITRATE
             preset='fast'     # PRESET FOR ENCODING
         )
        NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS: DO NOT USE SQUARE [] BRACKETS IN OUTPUT PATH !
        EXAMPLE_1 - input_files= [r"PATH_TO_INPUT_FILE"]     # SINGLE CONVERTION

        EXAMPLE_2 - input_files=[
                                r"PATH_TO_INPUT_FILE_1",
                                r"PATH_TO_INPUT_FILE_2" ]    # MULTIPLE CONVERTION

        >>> EXTRA: ALSO USE "bv" FOR BETTER QUALITY AND "present" FOR FAST CONVERTION.

        preset='ultrafast',    # PRESET FOR ENCODING
        bv='20M'               # VIDEO BITRATE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
            >>> NOTE ⇨ CONVERTING VIDEO TO AUDIO :
        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        from MediaSwift import *
        ffpe_instance = ffpe()

        # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        input_files = [ r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE' ]     # input_files [MULTIPLE CONVERT]
        output_dir =    r"PATH_TO_INPUT_FILE"

        # PERFORM MULTIMEDIA FILE CONVERSION USING FFPE.
        ffpe_instance.convert(
            input_files=input_files,
            output_dir=output_dir,
            hwaccel="cuda",   # HARDWARE ACCELERATION
            ar=44100,         # AUDIO SAMPLE RATE
            ac=2,             # AUDIO CHANNELS
            ba="192k",        # AUDIO BITRATE
            f="mp3",          # OUTPUT FORMAT (MP3 for audio)
            bv='50m',         # VIDEO BITRATE

        )

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ```
    ⇨ CODEC'S( )
    -------------
        >>> GET INFORMATION ABOUT AVAILABLE CODECS USING FFMPEG.

    ⇨ FORMAT'S( )
    -------------
       >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.

    >>> RETURNS: NONE

    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPE INSTANCE.

        >>> SETS THE DEFAULT PATH TO THE FFMPEG EXECUTABLE AND INITIALIZES THE LOGGER.
        """
        self.ffpe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffpe.exe"
        )
        self.logger = self._initialize_logger()

        self._ffprobe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffpr.exe"
        )

    def _initialize_logger(self) -> logging.Logger:
        """
        >>> INITIALIZE THE LOGGER FOR LOGGING MESSAGES.

        RETURNS:
        --------

        >>> LOGGING.LOGGER.
            >>> LOGGER INSTANCE.
        """
        logger = logging.getLogger("ffpe_logger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def convert(
        self,
        input_files: Optional[List[str]] = None,
        output_dir: Optional[str] = None,
        cv: Optional[str] = None,
        ca: Optional[str] = None,
        s: Optional[str] = None,
        hwaccel: Optional[str] = None,
        ar: Optional[int] = None,
        ac: Optional[int] = None,
        ba: Optional[int] = None,
        r: Optional[int] = None,
        f: Optional[str] = None,
        preset: Optional[str] = None,
        bv: Optional[int] = None,
    ) -> None:
        """
            >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         # INSTANTIATE THE FFPE CLASS

         from MediaSwift import *
         ffpe_instance = ffpe()

         # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        ... input_files = [ r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE' ]     # input_files [MULTIPLE CONVERT]
        ... input_files = [ r'PATH_TO_INPUT_FILE' ]                            # input_files [SINGLE CONVERT]

         output_dir = r'output_folder'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG.
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba='192k',        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             bv='50m',         # VIDEO BITRATE
             preset='fast'     # PRESET FOR ENCODING
         )
        NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS: DO NOT USE SQUARE [] BRACKETS IN OUTPUT PATH !
        EXAMPLE_1 ⇨ input_files= [ r"PATH_TO_INPUT_FILE" ]    # SINGLE CONVERTION

        EXAMPLE_2 ⇨ input_files=[
                                r"PATH_TO_INPUT_FILE_1",
                                r"PATH_TO_INPUT_FILE_2" ]    # MULTIPLE CONVERTION


        >>> EXTRA: ALSO USE "bv" FOR BETTER QUALITY AND "present" FOR FAST CONVERTION.

        preset='ultrafast',    # PRESET FOR ENCODING
        bv='20M'               # VIDEO BITRATE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        ```python
        >>> NOTE ⇨ CONVERTING VIDEO TO AUDIO :
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


        from MediaSwift import *
        ffpe_instance = ffpe()

        # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        input_files = [ r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE' ]         # input_files [MULTIPLE CONVERT]
        output_dir =    r"PATH_TO_INPUT_FILE"

        # PERFORM MULTIMEDIA FILE CONVERSION USING FFPE.
        ffpe_instance.convert(
            input_files=input_files,
            output_dir=output_dir,
            hwaccel="cuda",   # HARDWARE ACCELERATION
            ar=44100,         # AUDIO SAMPLE RATE
            ac=2,             # AUDIO CHANNELS
            ba="192k",        # AUDIO BITRATE
            f="mp3",          # OUTPUT FORMAT (MP3 for audio)
        )

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ```
        ⇨ ADDITIONAL NOTE:
        -------------------
        >>> REMEMBER ALWAYS USE SQUARE [] BRACKETS FOR INPUT FILES PATH.
        >>> RETURNS: NONE
        """

        if not input_files:
            self.logger.error("ERROR: NO INPUT FILES PROVIDED.")
            return

        if not output_dir:
            self.logger.error("ERROR: OUTPUT DIRECTORY NOT PROVIDED.")
            return

        if not isinstance(input_files, list):
            input_files = [input_files]

        # CHECK IF THE INPUT FILES EXIST
        for input_file in input_files:
            if not os.path.exists(input_file):
                self.logger.error(f"INVALID INPUT FILE PATH: {input_file}")
                return

        # DISPLAY DIFFERENT MESSAGES BASED ON THE USER'S CHOICE
        if len(input_files) > 1:
            clear_console()
            console.print(
                Panel(
                    f"[bold yellow]CONVERTING MULTIPLE MEDIA FILES ⇌  {len(input_files)}[/bold yellow]",
                    width=45,
                )
            )
        elif len(input_files) == 1:
            clear_console()
            console.print(
                Panel(
                    f"[bold yellow]CONVERTING SINGLE MEDIA FILE ⇌  {len(input_files)}[/bold yellow]",
                    width=45,
                )
            )

        # console.print(
        #     "[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold magenta]\n"
        # )

        for i, input_file in enumerate(input_files, start=1):
            filename = os.path.basename(input_file)
            output_file = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.{f}"
            )

            # CREATE A NEW TQDM INSTANCE FOR EACH FILE CONVERSION.
            progress_bar = tqdm(
                total=100,
                desc=f"⇨ CONVERTING [{i}]",
                unit="%",
                dynamic_ncols=True,
                bar_format="{l_bar}{bar:40}| {n_fmt}/{total_fmt} - TIME: {elapsed}",
                colour="green",
            )

            self.convert_single(
                input_file,
                output_file,
                cv,
                ca,
                s,
                hwaccel,
                ar,
                ac,
                ba,
                r,
                f,
                preset,
                bv,
                progress_bar,
            )

            progress_bar.close()

            # Display conversion completion message
            console.print(f"[bold red]⇨ CONVERSION FILE [{i}] COMPLETED ✅[/bold red]")

        console.print(
            Panel("[bold green]⇨ ALL CONVERSIONS COMPLETED ✅[/bold green]", width=40)
        )

    @lru_cache(maxsize=None)
    def convert_single(
        self,
        input_file: str,
        output_file: str,
        cv: Optional[str] = None,
        ca: Optional[str] = None,
        s: Optional[str] = None,
        hwaccel: Optional[str] = None,
        ar: Optional[int] = None,
        ac: Optional[int] = None,
        ba: Optional[int] = None,
        r: Optional[int] = None,
        f: Optional[str] = None,
        preset: Optional[str] = None,
        bv: Optional[int] = None,
        progress_bar: Optional[tqdm] = None,
    ) -> None:
        """

            >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         # INSTANTIATE THE FFPE CLASS.

         from MediaSwift import *
         ffpe_instance = ffpe()

         # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        ... input_files = [ r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE' ]        # input_files [MULTIPLE CONVERT]
        ... input_files = [ r'PATH_TO_INPUT_FILE' ]                               # input_files [SINGLE CONVERT]

         output_dir = r'output_folder'

         # PERFORM MULTIMEDIA FILE CONVERSION USING FFMPEG.
         ffpe_instance.convert(
             input_files=input_files,
             output_dir=output_dir,
             cv='h264',        # VIDEO CODEC
             ca='aac',         # AUDIO CODEC
             s='1920x1080',    # VIDEO RESOLUTION
             hwaccel='cuda',   # HARDWARE ACCELERATION
             ar=44100,         # AUDIO SAMPLE RATE
             ac=2,             # AUDIO CHANNELS
             ba='192k',        # AUDIO BITRATE
             r=30,             # VIDEO FRAME RATE
             f='mp4',          # OUTPUT FORMAT
             preset='fast'     # PRESET FOR ENCODING
         )
        NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS: DO NOT USE SQUARE [] BRACKETS IN OUTPUT PATH !
        EXAMPLE_1 ⇨ input_file= r"PATH_TO_INPUT_FILE"     # SINGLE CONVERTION

        EXAMPLE_2 ⇨ input_files=[
                                r"PATH_TO_INPUT_FILE_1",
                                r"PATH_TO_INPUT_FILE_2" ] # MULTIPLE CONVERTION.

        >>> EXTRA: ALSO USE "bv" FOR BETTER QUALITY AND "present" FOR FAST CONVERTION.

        preset='ultrafast',    # PRESET FOR ENCODING
        bv='20M'               # VIDEO BITRATE

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
                >>> NOTE ⇨ CONVERTING VIDEO TO AUDIO :
        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        from MediaSwift import *
        ffpe_instance = ffpe()

        # DEFINE INPUT FILES AND OUTPUT DIRECTORY.
        input_files = [ r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE' ]         # input_files [MULTIPLE CONVERT]
        output_dir =    r"PATH_TO_INPUT_FILE"

        # PERFORM MULTIMEDIA FILE CONVERSION USING FFPE.
        ffpe_instance.convert(
            input_files=input_files,
            output_dir=output_dir,
            hwaccel="cuda",   # HARDWARE ACCELERATION
            ar=44100,         # AUDIO SAMPLE RATE
            ac=2,             # AUDIO CHANNELS
            ba="192k",        # AUDIO BITRATE
            f="mp3",          # OUTPUT FORMAT (MP3 FOR AUDIO)
        )

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ```
        ⇨ ADDITIONAL NOTE:
        --------------------
        >>> REMEMBER ALWAYS USE SQUARE BRACKETS FOR INPUT FILE PATH.
        >>> RETURNS: NONE

        """
        # BUILD THE FFMPEG COMMAND BASED ON THE PROVIDED PARAMETERS.
        command = [self.ffpe_path, "-hide_banner"]

        if hwaccel:
            command += ["-hwaccel", hwaccel]

        command += ["-i", input_file]

        if cv:
            command += ["-c:v", cv]
        if ca:
            command += ["-c:a", ca]
        if s:
            s = s.replace("×", "x")
            command += ["-s", s]
        if ar:
            command += ["-ar", str(ar)]
        if ac:
            command += ["-ac", str(ac)]
        if ba:
            command += ["-b:a", str(ba)]
        if r:
            command += ["-r", str(r)]
        if f:
            command += ["-f", f]
        if preset:
            command += ["-preset", preset]
        if bv:
            command += ["-b:v", str(bv)]

        if output_file:
            command += ["-y", output_file]

        try:
            duration = self.get_duration(self, input_file)

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding="utf-8",
                shell=True,
                bufsize=1,
            )

            for line in process.stdout:
                match = re.search(r"time=(\d+:\d+:\d+.\d+)", line)
                if match:
                    time_str = match.group(1)
                    h, m, s = map(float, time_str.split(":"))
                    elapsed_time = h * 3600 + m * 60 + s
                    progress = min(elapsed_time / duration, 1.0)

                    # UPDATE TQDM PROGRESS USING NUMPY.CEIL TO ROUND UP
                    progress_percentage = int(np.ceil(progress * 100))
                    progress_bar.update(progress_percentage - progress_bar.n)

            # ENSURE THE PROGRESS BAR IS AT 100%
            progress_bar.n = 100
            progress_bar.refresh()

            # CLOSE THE PROGRESS BAR
            progress_bar.close()

        except subprocess.CalledProcessError as e:
            clear_console()
            print(f"FFPE COMMAND FAILED WITH ERROR: {e}")
        except Exception as e:
            clear_console()
            print(f"AN ERROR OCCURRED: {e}")

        gc.collect()

    @staticmethod
    def get_duration(self, file_path):
        command = f'{self._ffprobe_path} -v error -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 "{file_path}"'
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        durations = np.fromstring(output, sep="\r\n")
        return np.max(durations)

    @lru_cache(maxsize=None)
    def codecs(
        self, encoder: str = None
    ) -> None:  # CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES.
        """
            >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            >>> from MediaSwift import *
            >>> info = ffpe()
            >>> info.formats()

            # GET INFORMATION ABOUT THE CODEC'S ENCODER.
            >>> info.codecs(encoder="aac")
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

        >>> RETURNS: NONE
        """
        command = (
            [self.ffpe_path, "-h", f"encoder={encoder}"]
            if encoder
            else [self.ffpe_path, "-codecs"]
        )
        console = Console()

        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            lines = output.split("\n")

            if encoder:
                # DISPLAY DETAILED INFORMATION ABOUT THE SPECIFIED ENCODER
                table = Table(
                    show_header=True, header_style="bold magenta", box=ROUNDED
                )
                table.add_column("PROPERTY", style="cyan", width=60)
                table.add_column("VALUE", style="green", width=100)

                for line in lines[1:]:  # SKIP THE HEADER LINE
                    if (
                        line and ":" in line
                    ):  # SKIP EMPTY LINES AND LINES WITHOUT A COLON
                        property, value = line.split(":", 1)
                        property = (
                            property.strip().upper() if property.strip() else "NONE"
                        )
                        value = value.strip().upper() if value.strip() else "NONE"
                        table.add_row(property, value)
                        table.add_row("", "")  # ADD AN EMPTY ROW FOR SPACING

                console.print(table)

            else:
                # USE RICH TABLE FOR FORMATTING
                table = Table(
                    show_header=True, header_style="bold magenta", box=ROUNDED
                )
                table.add_column("CODECS", style="cyan", width=20)
                table.add_column("TYPE", style="green", width=25)
                table.add_column("DESCRIPTION", style="yellow", width=100)
                table.add_column("FEATURES", style="cyan", width=20)

                for line in lines[11:]:  # SKIP THE HEADER LINES
                    if line:  # SKIP EMPTY LINES
                        fields = line.split()
                        if len(fields) >= 4:  # ENSURE THERE ARE ENOUGH FIELDS
                            codec_name = fields[1]
                            codec_type = fields[2].strip("()")
                            codec_description = " ".join(fields[3:])
                            features = fields[0]

                            features_str = (
                                (".D" if "D" in features else "")
                                + (".E" if "E" in features else "")
                                + (".V" if "V" in features else "")
                                + (".A" if "A" in features else "")
                                + (".S" if "S" in features else "")
                                + (".T" if "T" in features else "")
                                + (".I" if "I" in features else "")
                                + (".L" if "L" in features else "")
                            )

                            table.add_row(
                                codec_name, codec_type, codec_description, features_str
                            )

                legend = "\n".join(
                    [
                        "[bold magenta]CODECS FEATURES LEGEND:[/bold magenta]",
                        "[cyan] D.....[/cyan] = DECODING SUPPORTED",
                        "[cyan] .E....[/cyan] = ENCODING SUPPORTED",
                        "[green] ..V...[/green] = VIDEO CODEC",
                        "[green] ..A...[/green] = AUDIO CODEC",
                        "[green] ..S...[/green] = SUBTITLE CODEC",
                        "[cyan] ..D...[/cyan] = DATA CODEC",
                        "[cyan] ..T...[/cyan] = ATTACHMENT CODEC",
                        "[cyan] ...I..[/cyan] = INTRA FRAME-ONLY CODEC",
                        "[cyan] ....L.[/cyan] = LOSSY COMPRESSION",
                        "[cyan] .....S[/cyan] = LOSSLESS COMPRESSION",
                    ]
                )
                console.print(legend)
                console.print("━━━━━━━━━━━━━━━━━━━━━━")
                console.print(table)

        except subprocess.CalledProcessError as e:
            clear_console()
            console.print(f"[bold red]FFPE COMMAND FAILED WITH ERROR: {e}[/bold red]")
        except Exception as e:
            clear_console()
            console.print(f"[bold red]AN ERROR OCCURRED: {e}[/bold red]")

        gc.collect()

    @lru_cache(maxsize=None)
    def formats(self) -> None:  # CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES.
        """
            >>> GET INFORMATION ABOUT AVAILABLE FORMATS USING FFMPEG.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            >>> from MediaSwift import *
            >>> info = ffpe()
            >>> info.formats()
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

        >>> RETURNS: NONE
        """
        command = [self.ffpe_path, "-formats"]
        console = Console()

        try:
            # IMPORT THE TABLE CLASS.
            from rich.table import Table

            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            lines = output.split("\n")

            # USE RICH TABLE FOR FORMATTING.
            table = Table(show_header=True, header_style="bold magenta", box=ROUNDED)
            table.add_column("FORMAT", style="cyan", width=30)
            table.add_column("DESCRIPTION", style="yellow", width=50)
            table.add_column("FEATURES", style="cyan", width=50)

            for line in lines[5:]:  # SKIP THE HEADER LINES.
                if line:  # SKIP EMPTY LINES.
                    fields = line.split()
                    if len(fields) >= 2:  # ENSURE THERE ARE ENOUGH FIELDS.
                        format_name = fields[1]
                        format_description = " ".join(fields[2:])
                        features = fields[0]

                        # EXTRACTING ADDITIONAL FEATURES.
                        features_str = (
                            (".D" if "D" in features else "")
                            + (".E" if "E" in features else "")
                            + (".V" if "V" in features else "")
                            + (".A" if "A" in features else "")
                            + (".S" if "S" in features else "")
                            + (".T" if "T" in features else "")
                            + (".I" if "I" in features else "")
                            + (".L" if "L" in features else "")
                        )

                        table.add_row(format_name, format_description, features_str)

            legend = "\n".join(
                [
                    "[bold magenta]FILE FORMATS FEATURES LEGEND:[/bold magenta]",
                    "[green] D.[/green] = DEMUXING SUPPORTED",
                    "[cyan] .E[/cyan] = MUXING SUPPORTED",
                ]
            )
            console.print(legend)
            console.print("━━━━━━━━━━━━━━━━━━━━━━")
            console.print(table)
        except subprocess.CalledProcessError as e:
            clear_console()
            console.print(f"[bold red]FFPE COMMAND FAILED WITH ERROR: {e}[/bold red]")
        except Exception as e:
            clear_console()
            console.print(f"[bold red]AN ERROR OCCURRED: {e}[/bold red]")

        gc.collect()

    @lru_cache(maxsize=None)
    def hwaccels(self) -> None:
        """
        >>> GET INFORMATION ABOUT AVAILABLE HARDWARE ACCELERATION METHODS USING FFPE.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            >>> from MediaSwift import *
            >>> info = ffpe()
            >>> info.hwaccels()
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURNS: NONE
        """
        command = [self.ffpe_path, "-hwaccels"]
        console = Console()

        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            output = result.stdout.decode("utf-8")
            hwaccels = output.strip().split("\n")

            table = Table(show_header=True, header_style="bold magenta", box=ROUNDED)
            table.add_column("HARDWARE ACCELERATION METHODS", style="cyan", width=50)

            # SKIP THE FIRST LINE IN THE OUTPUT
            for hwaccel in hwaccels[1:]:
                table.add_row(hwaccel)
            console.print(table)

        except subprocess.CalledProcessError as e:
            clear_console()
            console.print(f"[bold red]FFPE COMMAND FAILED WITH ERROR: {e}[/bold red]")
        except Exception as e:
            clear_console()
            console.print(f"[bold red]AN ERROR OCCURRED: {e}[/bold red]")

        gc.collect()

    @lru_cache(maxsize=None)
    def MediaClip(
        self,
        input_file: str,
        output_file: str,
        start_time: str,
        duration: str,
        fps: Optional[int] = None,
    ) -> None:
        """
        >>> EXTRACTS SPECIFIC PART OF VIDEO AND CONVERTS IT TO GIF.

        PARAMETERS:
        -----------
        >>> INPUT_FILE (STR): PATH TO THE INPUT VIDEO FILE.
        >>> OUTPUT_FILE (STR): PATH TO THE OUTPUT GIF FILE.
        >>> START_TIME (STR): START TIME OF THE CLIP (FORMAT: MM:SS).
        >>> DURATION (STR): DURATION OF THE CLIP (FORMAT: MM:SS).
        >>> FPS (OPTIONAL[INT]): FRAMES PER SECOND FOR THE OUTPUT GIF. IF NONE, THE ORIGINAL FPS WILL BE USED.

        >>> RETURNS: NONE
        """
        try:
            # BUILD THE FFMPEG COMMAND BASED ON THE PROVIDED PARAMETERS.
            command = [
                self.ffpe_path,
                "-hide_banner",
                "-i",
                input_file,
                "-ss",
                start_time,
                "-t",
                duration,
                "-vf",
                "scale=-1:-1:flags=lanczos",
            ]

            if fps is not None:
                command += ["-r", str(fps)]

            command += ["-y", output_file]

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding="utf-8",
                shell=True,
                bufsize=1,
            )

            for line in process.stdout:
                print(line, end="")

            print(f"\nMEDIACLIP COMPLETED: {output_file}")

        except subprocess.CalledProcessError as e:
            clear_console()
            print(f"MEDIACLIP FAILED WITH ERROR: {e}")
        except Exception as e:
            clear_console()
            print(f"AN ERROR OCCURRED: {e}")

        gc.collect()

    @lru_cache(maxsize=None)
    def MediaClip(
        self,
        input_file: str,
        output_file: str,
        time_range: str,
        fps: Optional[int] = None,
    ) -> None:
        """

        >>> EXTRACTS SPECIFIC PART OF VIDEO AND CONVERTS IT TO GIF.

        PARAMETERS:
        -----------
        >>> INPUT_FILE (STR): PATH TO THE INPUT VIDEO FILE.
        >>> OUTPUT_FILE (STR): PATH TO THE OUTPUT GIF FILE.
        >>> TIME_RANGE (STR): TIME RANGE OF THE CLIP (FORMAT: MM:SS,MM:SS).
        >>> FPS (OPTIONAL[INT]): FRAMES PER SECOND FOR THE OUTPUT GIF. IF NONE, THE ORIGINAL FPS WILL BE USED.

        ```python

        >>> EXAMPLE
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        from MediaSwift import *

        CONVERTER = ffpe()
        INPUT_FILE = r"PATH_TO_INPUT_FILE"  # INPUT FILE
        OUTPUT_FILE = r"PATH_TO_INPUT_FILE"  # OUTPUT FILE
        TIME_RANGE = "01:30,02:30"  # CLIP FROM 1 MINUTE 30 SECONDS TO 2 MINUTES 30 SECONDS

        CONVERTER.MediaClip(INPUT_FILE, OUTPUT_FILE, TIME_RANGE)

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        ```

        >>> RETURNS: NONE
        """
        try:
            start_time, end_time = map(str.strip, time_range.strip("()").split(","))
            start_seconds = sum(
                float(x) * 60**i for i, x in enumerate(reversed(start_time.split(":")))
            )
            end_seconds = sum(
                float(x) * 60**i for i, x in enumerate(reversed(end_time.split(":")))
            )
            duration_seconds = end_seconds - start_seconds

            # BUILD THE FFMPEG COMMAND BASED ON THE PROVIDED PARAMETERS.
            command = [
                self.ffpe_path,
                "-hide_banner",
                "-i",
                input_file,
                "-ss",
                f"{int(start_seconds)}",  # CONVERT START TIME TO INTEGER (WITHOUT FRACTIONS)
                "-t",
                f"{int(duration_seconds):.0f}",  # CONVERT DURATION TO INTEGER (WITHOUT FRACTIONS)
                "-vf",
                "scale=-1:-1:flags=lanczos",
            ]

            if fps is not None:
                command += ["-r", str(fps)]

            command += ["-y", output_file]

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                shell=True,
                bufsize=1,
                universal_newlines=True,
            )

            os.system("cls")
            console.print(
                Panel(
                    "[bold yellow]MEDIACLIP FILE CONVERTION.. [/bold yellow]", width=35
                )
            )
            # console.print(
            #     "[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold magenta]\n"
            # )
            
            with tqdm(
                total=100,
                desc="MEDIACLIP",
                unit="%",
                dynamic_ncols=True,
                bar_format="{l_bar}{bar:40}| {n_fmt}/{total_fmt} - TIME: {elapsed}",
            ) as progress_bar:
                for line in process.stderr:
                    match = re.search(r"time=(\d+:\d+:\d+.\d+)", line)
                    if match:
                        time_str = match.group(1)
                        m, s = map(float, time_str.split(":")[1:])  # SKIP THE HOUR PART
                        elapsed_time = m * 60 + s
                        progress = min(elapsed_time / duration_seconds, 1.0)

                        # UPDATE TQDM PROGRESS USING NUMPY.CEIL TO ROUND UP
                        progress_percentage = int(np.ceil(progress * 100))
                        progress_bar.update(progress_percentage - progress_bar.n)

            console.print(
                Panel("[bold green]⇨ CONVERSION COMPLETED ✅[/bold green]", width=30)
            )
            time.sleep(5)
            os.system("cls")

        except subprocess.CalledProcessError as e:
            clear_console()
            print(f"MEDIACLIP FAILED WITH ERROR: {e}")
        except Exception as e:
            clear_console()
            print(f"AN ERROR OCCURRED: {e}")

        gc.collect()


# CALL THE GARBAGE COLLECTOR TO FREE UP RESOURCES.
