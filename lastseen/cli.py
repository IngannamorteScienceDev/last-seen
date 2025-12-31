import logging
from pathlib import Path

from lastseen.logging import setup_logging
from lastseen.parser import parse_dialog_folder
from lastseen.exporter.json_export import export_messages_to_json


def main() -> None:
    setup_logging(logging.INFO)

    print("Last Seen — offline VK dialog viewer")

    dialog_path = Path("samples/486429703")
    output_path = Path("export/messages.json")

    messages = parse_dialog_folder(dialog_path)
    export_messages_to_json(messages, output_path)

    print(f"Exported {len(messages)} messages to {output_path}")


if __name__ == "__main__":
    main()
