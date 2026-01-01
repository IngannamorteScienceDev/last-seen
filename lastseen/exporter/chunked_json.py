"""
Last Seen — Chunked JSON Exporter
---------------------------------
Writes:
- export/meta.json
- export/date_index.json
- export/pages/page_XXX.json

Messages must be sorted chronologically (old -> new).
"""

from __future__ import annotations

import json
from math import ceil
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_PAGE_SIZE = 100


def export_chunked_dialog(
    messages: List[Dict[str, Any]],
    export_dir: str | Path = "export",
    page_size: int = DEFAULT_PAGE_SIZE,
) -> Dict[str, Any]:
    """
    Export dialog messages into chunked JSON format + date index.

    This function name MUST exist because CLI imports it.
    """
    if not messages:
        raise ValueError("No messages to export")

    export_dir = Path(export_dir)
    pages_dir = export_dir / "pages"

    export_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)

    total_messages = len(messages)
    total_pages = ceil(total_messages / page_size)

    # Build date index: first message of each date -> (page, offset)
    date_index: Dict[str, Dict[str, int]] = {}
    for global_idx, msg in enumerate(messages):
        dt = msg.get("datetime")
        if not dt or "T" not in dt:
            continue
        date = dt.split("T")[0]
        if date not in date_index:
            date_index[date] = {
                "page": global_idx // page_size,
                "offset": global_idx % page_size,
            }

    # Write pages
    for page in range(total_pages):
        start = page * page_size
        end = min((page + 1) * page_size, total_messages)
        chunk = messages[start:end]

        out = {
            "page": page,
            "page_size": page_size,
            "count": len(chunk),
            "messages": chunk,
        }

        with open(pages_dir / f"page_{page:03d}.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

    # Meta
    date_from = messages[0]["datetime"].split("T")[0] if messages[0].get("datetime") else None
    date_to = messages[-1]["datetime"].split("T")[0] if messages[-1].get("datetime") else None

    meta = {
        "total_pages": total_pages,
        "total_messages": total_messages,
        "page_size": page_size,
        "date_range": {"from": date_from, "to": date_to},
    }

    with open(export_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    with open(export_dir / "date_index.json", "w", encoding="utf-8") as f:
        json.dump(date_index, f, ensure_ascii=False, indent=2)

    return meta
