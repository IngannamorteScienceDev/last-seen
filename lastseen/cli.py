"""
Last Seen — CLI
---------------
Offline VK dialog processor.

Pipeline:
1. Parse VK HTML archive (messages*.html)
2. Collect messages in chronological order
3. (Optional) Download media
4. Export messages as chunked JSON:
   - export/meta.json
   - export/date_index.json
   - export/pages/page_XXX.json
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Dict, Any

from tqdm import tqdm

from lastseen.parser.vk_html import parse_messages_page
from lastseen.downloader.media import download_dialog_media
from lastseen.exporter.chunked_json import export_chunked_dialog


# ------------------------------
# helpers
# ------------------------------

def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def find_html_pages(dialog_dir: Path) -> List[Path]:
    return sorted(dialog_dir.glob("messages*.html"))


# ------------------------------
# parsing
# ------------------------------

def parse_dialog(dialog_dir: Path) -> List[Dict[str, Any]]:
    pages = find_html_pages(dialog_dir)
    if not pages:
        raise FileNotFoundError("No messages*.html files found")

    info(f"Found {len(pages)} HTML pages")

    all_messages: List[Dict[str, Any]] = []

    for page in tqdm(
        pages,
        desc="Parsing message pages",
        unit="page",
        dynamic_ncols=True,
    ):
        messages = parse_messages_page(page)
        all_messages.extend(messages)

    info(f"Total messages parsed: {len(all_messages)}")
    return all_messages


# ------------------------------
# CLI
# ------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="lastseen",
        description="Last Seen — offline VK dialog processor",
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to dialog folder (e.g. samples/123456789)",
    )

    parser.add_argument(
        "-o", "--output",
        default="export",
        help="Output directory (default: ./export)",
    )

    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Messages per JSON page (default: 100)",
    )

    parser.add_argument(
        "--no-media",
        action="store_true",
        help="Skip downloading media attachments",
    )

    args = parser.parse_args()

    dialog_dir = Path(args.input)
    output_dir = Path(args.output)

    info("Last Seen — offline VK dialog processor")
    info(f"Parsing dialog folder: {dialog_dir}")

    # 1. Parse messages
    messages = parse_dialog(dialog_dir)

    # 2. Download media (optional)
    if args.no_media:
        info("Media download skipped (--no-media)")
    else:
        info("Downloading dialog media")
        download_dialog_media(messages, out_dir=output_dir)

    # 3. Export chunked JSON + date index
    info("Exporting messages as chunked JSON")

    export_chunked_dialog(
        messages,
        export_dir=output_dir,
        page_size=args.page_size,
    )

    info("Export completed")
    info(f"Meta file: {output_dir / 'meta.json'}")
    info(f"Date index: {output_dir / 'date_index.json'}")
    info(f"Pages dir : {output_dir / 'pages'}")
    info("Done")


if __name__ == "__main__":
    main()
