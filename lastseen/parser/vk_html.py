"""
VK messages HTML parser.

Parses VK messages*.html files into normalized message objects.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from bs4 import BeautifulSoup
from tqdm import tqdm

from lastseen.attachments.taxonomy import ATTACHMENT_TYPES

logger = logging.getLogger(__name__)

# -------------------------
# Helpers
# -------------------------

MONTHS_RU = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4,
    "мая": 5, "июн": 6, "июл": 7, "авг": 8,
    "сен": 9, "окт": 10, "ноя": 11, "дек": 12,
}


def parse_datetime_ru(text: str) -> datetime:
    match = re.search(
        r"(\d{1,2}) (\w+) (\d{4}) в (\d{1,2}:\d{2}:\d{2})",
        text
    )
    if not match:
        raise ValueError(f"Cannot parse datetime: {text}")

    day, month_ru, year, time_part = match.groups()
    month_key = month_ru[:3].lower()

    if month_key not in MONTHS_RU:
        raise ValueError(f"Unknown month: {month_ru}")

    month = MONTHS_RU[month_key]

    return datetime.strptime(
        f"{day}.{month}.{year} {time_part}",
        "%d.%m.%Y %H:%M:%S"
    )


def normalize_attachment(label: str, href: Optional[str]) -> Dict:
    label_lower = (label or "").lower()

    if "фотограф" in label_lower:
        atype = ATTACHMENT_TYPES["photo"]
    elif "стикер" in label_lower:
        atype = ATTACHMENT_TYPES["sticker"]
    elif "аудиозапис" in label_lower:
        atype = ATTACHMENT_TYPES["audio_track"]
    elif "файл" in label_lower and href and href.endswith(".ogg"):
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
# Parsers
# -------------------------

def parse_messages_page(path: Path) -> List[Dict]:
    logger.info(f"Parsing page: {path.name}")

    with open(path, encoding="windows-1251", errors="ignore") as f:
        soup = BeautifulSoup(f, "lxml")

    messages: List[Dict] = []
    raw_messages = soup.select("div.message")

    logger.info(f"Found {len(raw_messages)} messages")

    for msg in raw_messages:
        msg_id = int(msg.get("data-id"))

        header = msg.select_one("div.message__header")
        header_text = header.get_text(" ", strip=True)
        edited = bool(header.select_one(".message-edited"))

        author_link = header.select_one("a")
        if author_link:
            vk_id = None
            m = re.search(r"id(\d+)", author_link["href"])
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

        body = header.find_next_sibling("div")
        text = ""
        if body:
            parts = []
            for node in body.contents:
                if getattr(node, "name", None) == "div" and "kludges" in (node.get("class") or []):
                    break
                if isinstance(node, str):
                    parts.append(node)
                elif node.name == "br":
                    parts.append("\n")
                else:
                    parts.append(node.get_text())
            text = "".join(parts).strip()

        attachments = []
        kludges = msg.select_one("div.kludges")
        if kludges:
            for att in kludges.select("div.attachment"):
                desc = att.select_one("div.attachment__description")
                label = desc.get_text(strip=True) if desc else "Unknown"
                link = att.select_one("a.attachment__link")
                href = link["href"] if link else None
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


def parse_dialog_folder(folder_path: Path) -> List[Dict]:
    logger.info(f"Parsing dialog folder: {folder_path}")

    html_files = sorted(folder_path.glob("messages*.html"))
    logger.info(f"Found {len(html_files)} HTML pages")

    all_messages: List[Dict] = []

    for html_file in tqdm(html_files, desc="Parsing message pages", unit="page"):
        all_messages.extend(parse_messages_page(html_file))

    logger.info(f"Total messages parsed: {len(all_messages)}")

    all_messages.sort(key=lambda m: m["datetime"])
    return all_messages
