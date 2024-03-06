# ffpr.py
# ---------

import os
import gc
import json
import subprocess
from functools import lru_cache
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED

console = Console()


class FFProbeResult:
    """
    >>> REPRESENTS THE INFO OF "FFPR" ANALYSIS ON MULTIMEDIA FILE.

    ⇨ ATTRIBUTE'S
    ---------------
    >>> INFO : DICT
        >>> INFORMATION OBTAINED FROM FFPR.

    ⇨ METHOD'S
    -----------
    >>> DURATION() ⇨  OPTIONAL[FLOAT]:
        >>> GET THE DURATION OF THE MULTIMEDIA FILE.
    >>> BIT_RATE() ⇨  OPTIONAL[FLOAT]:
        >>> GET THE BIT RATE OF THE MULTIMEDIA FILE.
    >>> NB_STREAMS() ⇨  OPTIONAL[INT]:
        >>> GET THE NUMBER OF STREAMS IN THE MULTIMEDIA FILE.
    ⇨ STREAMS():
        >>> GET THE DETAILS OF INDIVIDUAL STREAMS IN THE MULTIMEDIA FILE.

        >>> EXAMPLE:


        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpr

        >>> FFPR = ffpr()
        >>> INFO = FFPR.probe(r"PATH_TO_MEDIA_FILE")
        >>> FFPR.pretty(INFO)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

    >>> USE "PRETTY()" FOR MORE BEAUTIFY CONTENT SHOW.
    >>> RETURN NONE
    """

    def __init__(self, info):
        self.info = info

    @property
    def DURATION(self) -> Optional[float]:
        try:
            return float(self.info["format"]["duration"])
        except (KeyError, ValueError):
            return None

    @property
    def BIT_RATE(self) -> Optional[float]:
        try:
            return int(self.info["format"]["bit_rate"]) / 1000
        except (KeyError, ValueError):
            return None

    @property
    def NB_STREAMS(self) -> Optional[int]:
        return self.info["format"].get("nb_streams")

    @property
    def STREAMS(self):
        return self.info["streams"]


class ffpr:
    """
    >>> CLASS FOR INTERFACING WITH FFPR TO ANALYZE MULTIMEDIA FILES.

    ⇨ METHOD'S
    -----------
    PROBE[ INPUT_FILE ] ⇨ OPTIONAL:
    --------------------------------
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.
    ⇨ PRETTY( INFO )
    -----------------
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY CONTENT.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpr

        >>> DETAILS = ffpr()
        >>> INFO = DETAILS.probe(r"PATH_TO_MEDIA_FILE")
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
    >>> RETURN: NONE
    """

    console = Console()  # DECLARE CONSOLE AT THE CLASS LEVEL.

    def __init__(self):
        self._ffprobe_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "bin", "ffpr.exe"
        )
        self.info = None

    @property
    def ffprobe_path(self):
        return self._ffprobe_path

    @lru_cache(maxsize=None)
    def probe(self, input_file) -> Optional[FFProbeResult]:
        """
        >>> ANALYZE MULTIMEDIA FILE USING FFPR AND RETURN THE RESULT.

        ⇨ PARAMETER'S
        --------------
        INPUT_FILE : STR
        -----------------
            >>> PATH TO THE MULTIMEDIA FILE.

        ⇨ OPTIONAL
        -----------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        try:
            # Check if the input file exists
            if not os.path.isfile(input_file):
                raise FileNotFoundError(f"FILE '{input_file}' NOT FOUND")

            command = [
                self.ffprobe_path,
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                input_file,
            ]
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            self.info = FFProbeResult(json.loads(result.stdout.decode("utf-8")))
            gc.collect()
            self.pretty(self.info)
            return self.info
        except FileNotFoundError as e:
            error_message = Text(f"ERROR: {e}", style="bold red")
            console.print(error_message)
            return None
        except subprocess.CalledProcessError as e:
            error_message = Text(f"ERROR: {e}", style="bold red")
            console.print(error_message)
            return None
        except Exception as e:
            error_message = Text(
                f"ERROR: AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red"
            )
            console.print(error_message)
            return None

    @lru_cache(maxsize=None)
    def pretty(self, info: FFProbeResult):
        """
        >>> PRINT READABLE SUMMARY OF THE FFPR ANALYSIS RESULT, MAKE BEAUTIFY MEDIA INFO SHOW.

        ⇨ PARAMETER'S
        --------------
        INFO
        -------
            >>> RESULT OF THE FFPR ANALYSIS.
            >>> RETURN: NONE
        """
        if not info:
            self.console.print(
                "[bold magenta]WARNING: NO INFORMATION AVAILABLE.[/bold magenta]"
            )
            return

        self.console.print(
            "\n[bold magenta]MEDIA FILE ANALYSIS SUMMARY:[/bold magenta]"
        )
        self.console.print("[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        table = Table(show_header=True, header_style="bold magenta", box=ROUNDED)
        table.add_column("[bold magenta]PROPERTY[/bold magenta]")
        table.add_column("[bold magenta]VALUE[/bold magenta]")

        table.add_row(
            "[bold magenta]FILE[/bold magenta]", info.info["format"]["filename"].upper()
        )

        try:
            bit_rate_kbps = info.BIT_RATE
            table.add_row(
                "[bold magenta]BIT RATE[/bold magenta]",
                f"{bit_rate_kbps} kbit/s".upper(),
            )
        except (AttributeError, KeyError, ValueError):
            table.add_row("[bold magenta]BIT RATE[/bold magenta]", "N/A")

        try:
            duration_seconds = info.DURATION
            minutes, seconds = divmod(duration_seconds, 60)
            table.add_row(
                "[bold magenta]DURATION[/bold magenta]",
                f"{int(minutes)}:{int(seconds)} min".upper(),
            )
        except (AttributeError, KeyError, ValueError):
            table.add_row("[bold magenta]DURATION[/bold magenta]", "N/A")

        table.add_row(
            "[bold magenta]NUMBER OF STREAMS[/bold magenta]",
            str(info.NB_STREAMS).upper(),
        )

        self.console.print(table)

        for i, stream in enumerate(info.STREAMS):
            stream_type = stream.get("codec_type", "N/A")
            stream_type_upper = (
                stream_type.upper()
                if stream_type.lower() in ["video", "audio"]
                else stream_type
            )  # CONVERT TO UPPERCASE ONLY IF IT'S "VIDEO" OR "AUDIO".

            title = Text(f"{stream_type_upper} STREAM {i + 1}", style="bold magenta")
            title.stylize("[underline]")

            self.console.print(title)

            sub_table = Table(
                show_header=True, header_style="bold magenta", box=ROUNDED
            )
            sub_table.add_column("[bold magenta]ATTRIBUTE[/bold magenta]")
            sub_table.add_column("[bold magenta]VALUE[/bold magenta]")

            sub_table.add_row(
                "[bold magenta]CODEC[/bold magenta]",
                str(stream.get("codec_name", "N/A")).upper(),
            )
            sub_table.add_row(
                "[bold magenta]PROFILE[/bold magenta]",
                str(stream.get("profile", "N/A")).upper(),
            )

            try:
                bit_rate_kbps = int(stream.get("bit_rate", "N/A")) / 1000
                sub_table.add_row(
                    "[bold magenta]BIT RATE[/bold magenta]",
                    f"{bit_rate_kbps} kbit/s".upper(),
                )
            except (KeyError, ValueError):
                sub_table.add_row("[bold magenta]BIT RATE[/bold magenta]", "N/A")

            sub_table.add_row(
                "[bold magenta]TYPE[/bold magenta]",
                str(stream.get("codec_type", "N/A")).upper(),
            )
            sub_table.add_row(
                "[bold magenta]LANGUAGE[/bold magenta]",
                (
                    stream["tags"].get("language", "N/A").upper()
                    if "tags" in stream
                    else "N/A"
                ),
            )

            if stream["codec_type"] == "video":
                sub_table.add_row(
                    "[bold magenta]RESOLUTION[/bold magenta]",
                    f"{stream.get('width', 'N/A')}x{stream.get('height', 'N/A')}".upper(),
                )
                sub_table.add_row(
                    "[bold magenta]DISPLAY ASPECT RATIO[/bold magenta]",
                    str(stream.get("display_aspect_ratio", "N/A")).upper(),
                )
                sub_table.add_row(
                    "[bold magenta]FRAME RATE[/bold magenta]",
                    str(stream.get("r_frame_rate", "N/A")).upper(),
                )
            elif stream["codec_type"] == "audio":
                sub_table.add_row(
                    "[bold magenta]CHANNELS[/bold magenta]",
                    str(stream.get("channels", "N/A")).upper(),
                )
                sub_table.add_row(
                    "[bold magenta]SAMPLE RATE[/bold magenta]",
                    str(stream.get("sample_rate", "N/A")).upper(),
                )

            self.console.print(sub_table)

        gc.collect()
