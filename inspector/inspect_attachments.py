"""
Last Seen — Archive Inspector
-----------------------------

This script scans a VK dialog archive folder and detects
ALL attachment types present in messages HTML files.

Purpose:
- Explore real attachment types before designing parsers
- Collect statistics about attachments
- Detect which attachments contain downloadable links

What it does NOT do:
- Does not download anything
- Does not modify files
- Does not build final JSON structures

Usage:
    python inspector/inspect_attachments.py <path_to_dialog_folder>

Example:
    python inspector/inspect_attachments.py samples/486429703
"""

from pathlib import Path
import sys
from collections import defaultdict

from bs4 import BeautifulSoup
from tqdm import tqdm


# -----------------------------
# Utility functions
# -----------------------------

def find_html_files(dialog_path: Path) -> list[Path]:
    """Return all messages*.html files sorted by name."""
    return sorted(dialog_path.glob("messages*.html"))


def open_html(path: Path) -> BeautifulSoup:
    """Open VK HTML file with correct encoding."""
    with open(path, "r", encoding="windows-1251", errors="ignore") as f:
        return BeautifulSoup(f, "lxml")


# -----------------------------
# Main inspection logic
# -----------------------------

def inspect_dialog(dialog_path: Path) -> None:
    if not dialog_path.exists() or not dialog_path.is_dir():
        print(f"[ERROR] Path does not exist or is not a directory: {dialog_path}")
        sys.exit(1)

    html_files = find_html_files(dialog_path)

    if not html_files:
        print("[ERROR] No messages*.html files found")
        sys.exit(1)

    print(f"[INFO] Dialog folder: {dialog_path}")
    print(f"[INFO] Found HTML files: {len(html_files)}")
    print()

    attachment_stats = defaultdict(int)
    attachment_with_link = defaultdict(int)
    attachment_examples = defaultdict(set)

    total_messages = 0
    total_attachments = 0

    for html_file in tqdm(html_files, desc="Scanning HTML files", unit="file"):
        soup = open_html(html_file)

        messages = soup.select("div.message")
        total_messages += len(messages)

        for message in messages:
            kludges = message.select_one("div.kludges")
            if not kludges:
                continue

            attachments = kludges.select("div.attachment")
            for att in attachments:
                total_attachments += 1

                desc_tag = att.select_one("div.attachment__description")
                if not desc_tag:
                    att_type = "UNKNOWN"
                else:
                    att_type = desc_tag.get_text(strip=True)

                attachment_stats[att_type] += 1

                link = att.select_one("a.attachment__link")
                if link and link.get("href"):
                    attachment_with_link[att_type] += 1
                    attachment_examples[att_type].add(link["href"])

    # -----------------------------
    # Final report
    # -----------------------------

    print("\n" + "=" * 60)
    print("ARCHIVE INSPECTION REPORT")
    print("=" * 60)

    print(f"Total HTML files scanned: {len(html_files)}")
    print(f"Total messages scanned:   {total_messages}")
    print(f"Total attachments found:  {total_attachments}")
    print()

    print("Attachment types detected:")
    print("-" * 60)

    for att_type in sorted(attachment_stats, key=lambda x: attachment_stats[x], reverse=True):
        count = attachment_stats[att_type]
        with_link = attachment_with_link.get(att_type, 0)

        print(f"- {att_type}")
        print(f"    occurrences : {count}")
        print(f"    with link   : {with_link}")

        examples = list(attachment_examples.get(att_type, []))[:2]
        for ex in examples:
            print(f"    example     : {ex}")

    print("\n[INFO] Inspection completed successfully.")


# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_attachments.py <dialog_folder>")
        sys.exit(1)

    dialog_dir = Path(sys.argv[1])
    inspect_dialog(dialog_dir)
