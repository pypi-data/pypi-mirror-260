# ffpl.py
# ---------

from rich.panel import Panel
from rich.console import Console
import os
import sys
import gc
import subprocess
from functools import lru_cache
import time
import threading
from pathlib import Path

console = Console(width=40)


class ffpl:
    """
    >>> CLASS FOR INTERFACING TO PLAY MULTIMEDIA FILES.

    ATTRIBUTES
    ----------
    >>> ⇨ FFPL_PATH : STR
        >>> PATH TO THE FFPL EXECUTABLE.

    METHODS
    -------
    >>> ⇨ PLAY(MEDIA_FILE)
        >>> PLAY MULTIMEDIA FILE.
    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >>> from MediaSwift import ffpl
    >>> play = ffpl()

    # INCREASE VOLUME BY 10 DB
    >>> volume = 5
    >>> media_file = r"PATH_TO_MEDIA_FILE"
    >>> play.play(media_file)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ```
    >>> RETURNS: NONE
    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPL INSTANCE.
        >>> SETS THE DEFAULT PATH TO THE FFPL EXECUTABLE.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"
        >>> play.play(media_file)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURN: NONE
        """
        self.ffplay_path = Path(__file__).resolve().parent / "bin" / "ffpl.exe"

    @lru_cache(maxsize=None)  # SETTING MAXSIZE TO NONE MEANS AN UNBOUNDED CACHE
    def play(self, media_file, volume=0):
        """
        >>> PLAY MULTIMEDIA FILE USING FFPL WITH SPECIFIED VIDEO FILTERS.

        ⇨ PARAMETER'S
        ------------
        >>> MEDIA_FILE : STR
           >>> PATH TO THE MULTIMEDIA FILE TO BE PLAYED.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> play = ffpl()
        >>> media_file = r"PATH_TO_MEDIA_FILE"
        
        # INCREASE VOLUME BY 10 DB
        >>> volume = 5
        >>> play.play(media_file, volume)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURNS: NONE

        """
        console_1 = Console(width=100)
        if not Path(media_file).exists():
            console_1.print(Panel(
                f"ERROR: THE FILE PATH [bold green]{media_file.upper()}[/bold green] DOES NOT EXIST.", style="bold red"
            ))
            return

        if not Path(media_file).is_file():
            console_1.print(Panel(f"ERROR: [bold green]{media_file.upper()}[/bold green] IS NOT A FILE PATH.", style="bold red"))
            return

        # MODIFY THE COMMAND TO INCLUDE THE OPTIONS FOR SETTING.
        command = [
            str(self.ffplay_path),
            "-hide_banner",
            "-fs",
            "-vf",
            "hqdn3d,unsharp",
            "-loglevel",
            "panic",
            "-af",
            f"volume={volume}dB",
            str(media_file),
        ]

        def clear():
            os.system("cls" if os.name == "nt" else "clear")
        
        
        def hide_cursor():
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
        
        
        def show_cursor():
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
        
        # PRINT A CYCLIC WAVE PATTERN TO CREATE AN ILLUSION OF A MOVING WAVE.
        def print_wave_pattern(stop_wave_pattern):
            hide_cursor()
            wave_pattern = "▅▆▇▆▅▄▃▄▅▆▇▆▅"
            while not stop_wave_pattern.is_set():
                # GET THE CURRENT WIDTH OF THE CONSOLE.
                console_width = console.width
                # SUBTRACT THE WIDTH OF THE PANEL'S BORDER.
                console_width -= 4  # ADJUST THIS VALUE IF NEEDEDF
                # TRUNCATE OR PAD THE WAVE PATTERN TO FIT WITHIN THE CONSOLE WIDTH.
                adjusted_wave_pattern = (
                    wave_pattern * (console_width // len(wave_pattern) + 1)
                )[:console_width]
                clear()
                console.print(Panel("MEDIA PLAYER. NOW PLAYING 🎵", style="bold green"))
                console.print(
                    Panel(adjusted_wave_pattern, style="bold black"), end="\r"
                )
                wave_pattern = wave_pattern[2:] + wave_pattern[:2]
                time.sleep(0.1)

        # CREATE AN EVENT TO SIGNAL THE THREAD TO STOP.
        stop_wave_pattern = threading.Event()

        # START A SEPARATE THREAD TO PRINT THE WAVE PATTERN.
        wave_thread = threading.Thread(
            target=print_wave_pattern, args=(stop_wave_pattern,)
        )
        wave_thread.daemon = True  # SET THE THREAD AS A DAEMON THREAD.
        wave_thread.start()

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            console.print(
                f"AN ERROR OCCURRED WHILE PLAYING THE MEDIA FILE: {e}", style="bold red"
            )
        except Exception as e:
            console.print(f"AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red")
        finally:
            # SIGNAL THE WAVE PATTERN THREAD TO STOP GRACEFULLY.
            stop_wave_pattern.set()
            wave_thread.join()  # WAIT FOR THE THREAD TO COMPLETE.

            clear()
            console.print(Panel("MEDIA PLAYER EXITED..", style="bold yellow"))
            time.sleep(2)
            clear()
            show_cursor()
            gc.collect()








