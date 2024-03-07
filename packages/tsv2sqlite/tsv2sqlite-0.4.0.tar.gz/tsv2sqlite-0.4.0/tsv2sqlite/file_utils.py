import hashlib
import logging
import os
import platform
import sys

from typing import Optional
from rich.console import Console
from datetime import datetime

error_console = Console(stderr=True, style="bold red")


def calculate_md5(file_path: str) -> str:
    """Calculate the md5 checksum for the specified file.

    Args:
        file_path (str): the file for which the md5 checksum will be calculated

    Returns:
        str: the calculated md5 checksum
    """
    md5_hash = hashlib.md5()
    logging.info(f"Will attempt to calculate the MD5 checksum for file '{file_path}'")

    with open(file_path, "rb") as file:
        # Read the file in chunks to efficiently handle large files
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def get_file_creation_date(file_path: str) -> datetime:
    """Determine the creation date for the specified file.

    Args:
        file_path (str): the absolute path of the file

    Returns:
        datetime: the date the file was created according to the operating system
    """
    if platform.system() == "Windows":
        # On Windows, use creation time
        creation_time = os.path.getctime(file_path)
    else:
        # On Unix-based systems, use birth time (creation time)
        # Note: Not all file systems support birth time, and it might not be available on some systems.
        stat_info = os.stat(file_path)
        creation_time = stat_info.st_mtime

    # Convert the timestamp to a readable date
    creation_date = datetime.fromtimestamp(creation_time)

    return creation_date

def check_infile_status(infile: str, extension: Optional[str] = None) -> None:
    """Check if the file exists, if it is a regular file and whether it has
    content.

    Args:
        infile (str): the file to be checked

    Raises:
        None
    """

    error_ctr = 0

    if infile is None or infile == "":
        error_console.print(f"'{infile}' is not defined")
        error_ctr += 1
    else:
        if not os.path.exists(infile):
            error_ctr += 1
            error_console.print(f"'{infile}' does not exist")
        else:
            if not os.path.isfile(infile):
                error_ctr += 1
                error_console.print(f"'{infile}' is not a regular file")
            if os.stat(infile).st_size == 0:
                error_console.print(f"'{infile}' has no content")
                error_ctr += 1
            if extension is not None and not infile.endswith(extension):
                error_console.print(
                    f"'{infile}' does not have filename extension '{extension}'"
                )
                error_ctr += 1

    if error_ctr > 0:
        error_console.print(f"Detected problems with input file '{infile}'")
        sys.exit(1)

