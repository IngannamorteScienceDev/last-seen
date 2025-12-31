import argparse
import logging
from pathlib import Path

from lastseen.logging import setup_logging
from lastseen.parser import parse_dialog_folder
from lastseen.exporter.json_export import export_messages_to_json


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="last-seen",
        description="Create an offline JSON mirror of a VK dialog from HTML archive"
    )

    parser.add_argument(
        "-i", "--input",
        type=Path,
        required=True,
        help="Path to dialog folder containing messages*.html files"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("export/messages.json"),
        help="Path to output JSON file (default: export/messages.json)"
    )

    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Parse dialog but do not export JSON file"
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    verbosity.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-critical output"
    )

    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    # Logging level
    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    setup_logging(log_level)

    logging.info("Last Seen — offline VK dialog processor")

    dialog_path: Path = args.input
    output_path: Path = args.output

    messages = parse_dialog_folder(dialog_path)

    if args.no_export:
        logging.info("Export skipped (--no-export)")
        return

    export_messages_to_json(messages, output_path)
    logging.info(f"Exported {len(messages)} messages to {output_path}")


if __name__ == "__main__":
    main()
