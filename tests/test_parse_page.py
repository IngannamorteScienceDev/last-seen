from pathlib import Path
from pprint import pprint

from lastseen.parser.vk_html import parse_messages_page


if __name__ == "__main__":
    # Path to any messages*.html file
    html_path = Path("samples/486429703/messages2050.html")

    messages = parse_messages_page(html_path)

    print(f"Parsed messages: {len(messages)}\n")

    for msg in messages[:3]:
        pprint(msg)
        print("-" * 80)
