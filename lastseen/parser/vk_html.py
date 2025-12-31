"""
VK messages HTML parser.

Parses a single messages*.html file and returns
a list of normalized message dictionaries.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Optional
import re
from datetime import datetime

from bs4 import BeautifulSoup

from lastseen.attachments.taxonomy import ATTACHMENT_TYPES


# -------------------------
# Helpers
# -------------------------

MONTHS_RU = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4,
    "мая": 5, "июн": 6, "июл": 7, "авг": 8,
    "сен": 9, "окт": 10, "ноя": 11, "дек": 12,
}


def parse_datetime_ru(text: str) -> datetime:
    """
    Parse datetime like: '5 мая 2022 в 1:34:19'
    """
    match = re.search(
        r"(\d{1,2}) (\w+) (\d{4}) в (\d{1,2}:\d{2}:\d{2})",
        text
    )
    if not match:
        raise ValueError(f"Cannot parse datetime: {text}")

    day, month_ru, year, time_part = match.groups()

    # We normalize month name by taking first 3 letters: "мая" -> "мая" (works),
    # "сентября" -> "сен" (works), etc.
    month_key = month_ru[:3].lower()
    if month_key not in MONTHS_RU:
        raise ValueError(f"Unknown month: {month_ru} in datetime: {text}")

    month = MONTHS_RU[month_key]

    return datetime.strptime(
        f"{day}.{month}.{year} {time_part}",
        "%d.%m.%Y %H:%M:%S"
    )


def normalize_attachment(label: str, href: Optional[str]) -> Dict:
    """
    Normalize VK attachment based on taxonomy and available href.
    """
    label_lower = (label or "").lower()

    if "фотограф" in label_lower:
        atype = ATTACHMENT_TYPES["photo"]
    elif "стикер" in label_lower:
        atype = ATTACHMENT_TYPES["sticker"]
    elif "аудиозапис" in label_lower:
        atype = ATTACHMENT_TYPES["audio_track"]
    elif "файл" in label_lower and href and href.lower().endswith(".ogg"):
        # In your archive, "Файл" with .ogg is effectively a voice message
        atype = ATTACHMENT_TYPES["voice_message"]
    elif "видеозапис" in label_lower:
        atype = ATTACHMENT_TYPES["video"]
    elif "прикрепл" in label_lower:
        atype = ATTACHMENT_TYPES["forwarded_messages"]
    elif "ссылка" in label_lower:
        atype = ATTACHMENT_TYPES["link"]
    elif "запись на стене" in label_lower:
        atype = ATTACHMENT_TYPES["wall_post"]
    elif "подарок" in label_lower:
        atype = ATTACHMENT_TYPES["gift"]
    elif "звонок" in label_lower:
        atype = ATTACHMENT_TYPES["call"]
    elif "история" in label_lower:
        atype = ATTACHMENT_TYPES["story"]
    elif "плейлист" in label_lower:
        atype = ATTACHMENT_TYPES["playlist"]
    elif "карта" in label_lower:
        atype = ATTACHMENT_TYPES["map"]
    else:
        atype = ATTACHMENT_TYPES["unknown"]

    return {
        "type": atype.key,
        "downloadable": atype.downloadable,
        "source": atype.source,
        "viewer": atype.viewer,
        "source_url": href,
        "local_path": None,
        "label": label,
    }


# -------------------------
# Main parser
# -------------------------

def parse_messages_page(path: Path) -> List[Dict]:
    """
    Parse a single VK messages HTML page: messages*.html
    """
    with open(path, encoding="windows-1251", errors="ignore") as f:
        soup = BeautifulSoup(f, "lxml")

    messages: List[Dict] = []

    for msg in soup.select("div.message"):
        data_id = msg.get("data-id")
        if not data_id:
            # Extremely defensive: should not happen, but we skip
            continue

        msg_id = int(data_id)

        header = msg.select_one("div.message__header")
        if header is None:
            # Skip malformed message blocks
            continue

        header_text = header.get_text(" ", strip=True)
        edited = bool(header.select_one(".message-edited"))

        # Author
        author_link = header.select_one("a")
        if author_link and author_link.get("href"):
            href = author_link["href"]
            # Usually "https://vk.com/id486429703"
            vk_id = None
            m = re.search(r"id(\d+)", href)
            if m:
                vk_id = int(m.group(1))

            author = {
                "role": "other",
                "name": author_link.get_text(strip=True),
                "vk_id": vk_id,
            }
        else:
            author = {
                "role": "self",
                "name": "Вы",
                "vk_id": None,
            }

        dt = parse_datetime_ru(header_text)

        # Message text: sibling <div> after header, with possible nested <div class="kludges">
        body_div = header.find_next_sibling("div")
        text = ""
        if body_div is not None:
            text_parts = []
            for node in body_div.contents:
                if getattr(node, "name", None) == "div" and "kludges" in (node.get("class") or []):
                    break
                if isinstance(node, str):
                    text_parts.append(node)
                elif getattr(node, "name", None) == "br":
                    text_parts.append("\n")
                else:
                    text_parts.append(node.get_text())

            text = "".join(text_parts).strip()

        # Attachments
        attachments = []
        kludges = msg.select_one("div.kludges")
        if kludges:
            for att in kludges.select("div.attachment"):
                desc = att.select_one("div.attachment__description")
                label = desc.get_text(strip=True) if desc else "Unknown"

                link = att.select_one("a.attachment__link")
                href = link.get("href") if link else None

                attachments.append(normalize_attachment(label, href))

        messages.append({
            "id": msg_id,
            "author": author,
            "datetime": dt.isoformat(),
            "edited": edited,
            "text": text,
            "attachments": attachments,
        })

    return messages

def parse_dialog_folder(folder_path: Path) -> list[dict]:
    """
    Parse all messages*.html files in a dialog folder
    and return a single list of messages.
    """
    if not folder_path.exists() or not folder_path.is_dir():
        raise ValueError(f"Dialog folder does not exist: {folder_path}")

    html_files = sorted(folder_path.glob("messages*.html"))
    if not html_files:
        raise ValueError(f"No messages*.html files found in {folder_path}")

    all_messages: list[dict] = []

    for html_file in html_files:
        page_messages = parse_messages_page(html_file)
        all_messages.extend(page_messages)

    # Sort messages by datetime (oldest -> newest)
    all_messages.sort(key=lambda m: m["datetime"])

    return all_messages

