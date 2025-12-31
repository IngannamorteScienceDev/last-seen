from pathlib import Path
import logging

from lastseen.logging import setup_logging
from lastseen.parser import parse_dialog_folder


if __name__ == "__main__":
    setup_logging(logging.INFO)

    dialog_path = Path("samples/486429703")
    messages = parse_dialog_folder(dialog_path)

    print(f"Parsed total messages: {len(messages)}")
