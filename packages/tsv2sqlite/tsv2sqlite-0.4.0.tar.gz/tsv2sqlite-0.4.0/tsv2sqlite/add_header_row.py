"""Add header row to tab-delimited file that has none."""
import logging
import os
import pathlib
import sys
from datetime import datetime
from pathlib import Path

import click
import yaml
from rich.console import Console

from tsv2sqlite.manager import Manager
from .file_utils import check_infile_status


DEFAULT_OUTDIR = os.path.join(
    "/tmp/tsv2sqlite/",
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "conf", "config.yaml"
)


DEFAULT_LOGGING_FORMAT = (
    "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"
)

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()



@click.command()
@click.option(
    "--config_file",
    type=click.Path(exists=True),
    help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'",
)
@click.option(
    "--infile",
    help="The input tab-delimited file to be parsed and loaded into the SQLite3 database",
)
@click.option("--logfile", help="The log file")
@click.option(
    "--outdir",
    help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option("--outfile", help="Optional: The output file to be created to which the new header row will be added - default is a file with same base name as the input file written to the output directory.")
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'",
)
def main(
    config_file: str,
    infile: str,
    logfile: str,
    outdir: str,
    outfile: str,
    verbose: bool,
):
    """Console script for tsv2sqlite."""

    error_ctr = 0

    if infile is None:
        console.print("[bold red]--infile was not specified[/]")
        error_ctr += 1

    if error_ctr > 0:
        return -1

    check_infile_status(infile)

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        console.print(
            f"[yellow]--config_file was not specified and therefore was set to '{config_file}'[/]"
        )

    check_infile_status(config_file)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(
            f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]"
        )

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        console.print(
            f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]"
        )

    if outfile is None:
        outfile = os.path.join(
            outdir, os.path.join(outdir, os.path.basename(infile))
        )
        console.print(
            f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]"
        )

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        console.print(
            f"[yellow]--verbose was not specified and therefore was set to '{verbose}'[/]"
        )

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    # Read the configuration from the JSON file and
    # load into dictionary.
    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    manager = Manager(
        config=config,
        config_file=config_file,
        outdir=outdir,
        logfile=logfile,
        infile=infile,
        verbose=verbose
    )

    manager.add_header(outfile)

    print(f"The log file is '{logfile}'")
    console.print(
        f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
