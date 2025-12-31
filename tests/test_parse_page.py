from pathlib import Path
import logging

from lastseen.logging import setup_logging
from lastseen.parser.vk_html import parse_messages_page


if __name__ == "__main__":
    setup_logging(logging.INFO)

    html_path = Path("samples/486429703/messages2050.html")
    messages = parse_messages_page(html_path)

    print(f"Parsed messages: {len(messages)}")
