"""
VK messages HTML parser.

Parses a single messages*.html file and returns
a list of normalized message dictionaries.
"""

from pathlib import Path
from typing import List, Dict, Optional
import re
from datetime import datetime

from bs4 import BeautifulSoup

from attachments.taxonomy import ATTACHMENT_TYPES


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
    # 5 мая 2022 в 1:34:19
    match = re.search(
        r"(\d{1,2}) (\w+) (\d{4}) в (\d{1,2}:\d{2}:\d{2})",
        text
    )
    if not match:
        raise ValueError(f"Cannot parse datetime: {text}")

    day, month_ru, year, time_part = match.groups()
    month = MONTHS_RU[month_ru[:3]]

    return datetime.strptime(
        f"{day}.{month}.{year} {time_part}",
        "%d.%m.%Y %H:%M:%S"
    )


def normalize_attachment(label: str, href: Optional[str]) -> Dict:
    """
    Normalize VK attachment based on taxonomy.
    """
    label_low_
