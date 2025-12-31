import logging
from pathlib import Path

from lastseen.logging import setup_logging
from lastseen.parser import parse_dialog_folder


def main() -> None:
    setup_logging(logging.INFO)

    print("Last Seen — offline VK dialog viewer")

    dialog_path = Path("samples/486429703")
    messages = parse_dialog_folder(dialog_path)

    print(f"Parsed {len(messages)} messages")


if __name__ == "__main__":
    main()
