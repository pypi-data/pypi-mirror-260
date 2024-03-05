import argparse
import logging
import sys
import time
import webbrowser
from pathlib import Path
from typing import Union

from cbsplotlib import __version__
from cbsplotlib.highcharts import HC_DEFAULTS_DIRECTORY

HC_HTML_VIEW_TEMPLATE = "highcharts_view.html"

_logger = logging.getLogger(__name__)


class HtmlViewer:
    def __init__(
        self,
        filename: Union[str, Path],
        output_html_file: Union[str, Path] = None,
        output_directory: Union[str, Path] = None,
        view_template: Union[str, Path] = None,
        view_template_directory: Union[str, Path] = None,
        show: bool = False,
        keep: bool = None,
        overwrite: bool = False,
    ):
        self.filename = Path(filename)

        if output_directory is None:
            self.output_directory = self.filename.parent
        else:
            self.output_directory = Path(output_directory)

        self.keep = keep

        if output_html_file is None:
            out_file_base = (
                "_".join([self.filename.stem, "rendered"]) + self.filename.suffix
            )
            if keep is None:
                self.keep = False
        else:
            out_file_base = Path(output_html_file)
            if keep is None:
                self.keep = True

        self.output_html_file = self.output_directory / out_file_base

        if self.keep and self.output_html_file.exists() and not overwrite:
            question = f"File {self.output_html_file} already exists.  Overwrite it? (Enter y/n)"
            answer = None
            while answer not in {"y", "n"}:
                answer = input(question).lower()
                if answer == "n":
                    sys.exit()
                elif answer == "y":
                    pass
                else:
                    print("Please enter 'y' or 'n'")

        self.view_template = view_template
        self.view_template_directory = view_template_directory

        html_contents = self.make_html_template()

        _logger.info(f"Writing to {self.output_html_file}")
        try:
            with open(self.output_html_file, "w", encoding="utf-8") as fp:
                fp.write(html_contents)
        except FileNotFoundError as err:
            _logger.warning(err)
            raise FileNotFoundError(
                "Run eerst de script highchart_example_line_with_datetimes.py "
                "om de html file te maken!"
            )

        if show:
            self.show()
        else:
            self.keep = True

    def make_html_template(self):
        if self.view_template_directory is not None:
            defaults_directory = self.view_template_directory
        else:
            defaults_directory = Path(__file__).parent / Path(HC_DEFAULTS_DIRECTORY)

        if self.view_template is not None:
            html_view_template = self.view_template
        else:
            html_view_template = HC_HTML_VIEW_TEMPLATE

        html_template_file = defaults_directory / html_view_template

        with open(html_template_file) as fp:
            html_template = fp.read()

        _logger.info(f"Reading  {self.filename}")
        with open(self.filename, mode="r", encoding="utf-8") as stream:
            highchart_script = stream.read()

        new_html = html_template.replace("HIGHCHARTS_SCRIPT", highchart_script)

        return new_html

    def show(self):

        url = "file://" + self.output_html_file.absolute().as_posix()

        _logger.info(f"Showing {url}")
        webbrowser.open(url)

    def clean(self):

        _logger.info(f"Remove {self.output_html_file}")
        self.output_html_file.unlink()


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as a list of strings, for example, ``["--help"]``.

    Returns:
      `argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Tool om latex tabulars in xls files om te zetten"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="highcharts_html_viewer {ver}".format(ver=__version__),
    )
    parser.add_argument("filename", help="Tabular file name", metavar="FILENAME")
    parser.add_argument(
        "--output_filename",
        help="Naam van de html output file. Moet extensie .html " "hebben",
        metavar="OUTPUT_FILENAME",
    )
    parser.add_argument(
        "--output_directory",
        help="Naam van de output directory. Als niet gegeven wordt het"
        "door de input filenaam bepaald",
        metavar="OUTPUT_DIRECTORY",
    )
    parser.add_argument(
        "--show_html",
        help="Open een browser en laat de html zien",
        action="store_true",
        default=True,
    )
    parser.add_argument(
        "--no_show_html",
        help="Laat de html niet zien. Impliceert keep is true",
        action="store_false",
        dest="show_html",
    )
    parser.add_argument(
        "--keep",
        help="Schrijf alleen de html maar laat nog niet zien",
        action="store_true",
    )
    parser.add_argument(
        "--overwrite", help="Forceer overschrijven", action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    log_format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    hc_view = HtmlViewer(
        filename=args.filename,
        output_html_file=args.output_filename,
        output_directory=args.output_directory,
        show=args.show_html,
        keep=args.keep,
        overwrite=args.overwrite,
    )

    if not hc_view.keep:
        time.sleep(10)
        hc_view.clean()


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
