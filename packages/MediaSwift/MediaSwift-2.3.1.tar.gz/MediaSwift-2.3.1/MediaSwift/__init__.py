# __init__.py
# -------------

"""
MEDIASWIFT - A PYTHON LIBRARY FOR MULTIMEDIA PROCESSING.
AUTHOR: ROHIT SINGH
"""


import os

from .ffpe import ffpe
from .ffpr import ffpr
from .ffpl import ffpl

__all__ = ["ffpe", "ffpr", "ffpl", "version", "author"]

__version__ = "2.3.1"

__author__ = "ROHIT SINGH"


def author():
    """
    >>> RETURNS THE LIBRARY AUTHOR NAME.

    RETURN:
    -------
        >>> STR: THE LIBRARY AUTHOR NAME.

    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    from MediaSwift import author

    info = author()
    print(info)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
    >>> RETURN: NONE
    """
    return "PYTHON LIBRARY AUTHOR NAME: " + __author__


def version():
    """
    >>> RETURNS THE LIBRARY VERSION.

    RETURN:
    -------
        >>> STR: THE LIBRARY VERSION.

    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    from MediaSwift import version

    info = version()
    print(info)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
    >>> RETURN: NONE
    """
    return "PYTHON LIBRARY VERSION: " + __version__


def add_ffmpeg_to_path():
    """
    >>> ADD THE LIBRARY'S FFMPEG BINARY PATH TO THE SYSTEM PATH.
    """
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path


add_ffmpeg_to_path()
