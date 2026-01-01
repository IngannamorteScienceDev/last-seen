import argparse
import json
from pathlib import Path

from tqdm import tqdm

from lastseen.parser.vk_html import parse_messages_page
from lastseen.downloader.media import download_attachments
from lastseen.exporter.chunked_json import export_chunked_dialog


def collect_html_pages(dialog_dir: Path):
    pages = sorted(dialog_dir.glob("messages*.html"))
    if not pages:
        raise FileNotFoundError("No messages*.html files found")
    return pages


def main():
    parser = argparse.ArgumentParser(
        description="Last Seen — offline VK dialog processor"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to dialog folder containing messages*.html files"
    )
    parser.add_argument(
        "--no-media",
        action="store_true",
        help="Skip media downloading"
    )

    args = parser.parse_args()

    dialog_dir = Path(args.input)
    export_dir = Path("export")
    export_dir.mkdir(exist_ok=True)

    print("[INFO] Last Seen — offline VK dialog processor")
    print(f"[INFO] Parsing dialog folder: {dialog_dir}")

    html_pages = collect_html_pages(dialog_dir)
    print(f"[INFO] Found {len(html_pages)} HTML pages")

    messages = []

    for html_path in tqdm(html_pages, desc="Parsing message pages", unit="page"):
        page_messages = parse_messages_page(html_path)
        messages.extend(page_messages)

    print(f"[INFO] Total messages parsed: {len(messages)}")

    if not args.no_media:
        attachments = []
        for msg in messages:
            attachments.extend(msg.get("attachments", []))

        print(f"[INFO] Downloading {len(attachments)} attachments")
        downloaded = download_attachments(attachments, export_dir / "media")
        print(f"[INFO] Downloaded {downloaded} new files")
    else:
        print("[INFO] Media download skipped (--no-media)")

    print("[INFO] Exporting messages as chunked JSON")
    export_chunked_dialog(
        messages=messages,
        output_dir=export_dir,
        page_size=100,
    )

    print("[INFO] Done")


if __name__ == "__main__":
    main()
