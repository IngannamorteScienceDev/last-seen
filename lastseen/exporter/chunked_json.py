from pathlib import Path
import json
from datetime import datetime
from typing import List, Dict


def export_chunked_dialog(
    messages: List[Dict],
    output_dir: Path,
    page_size: int = 100,
):
    """
    Export dialog messages into chunked JSON pages.

    Resulting structure:

    export/
    ├── meta.json
    └── pages/
        ├── page_000.json
        ├── page_001.json
        ├── page_002.json
        └── ...
    """

    output_dir = Path(output_dir)
    pages_dir = output_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    total_messages = len(messages)
    total_pages = (total_messages + page_size - 1) // page_size

    print(f"[INFO] Chunking {total_messages} messages into {total_pages} pages")

    # --- write pages ---
    for page_index in range(total_pages):
        start = page_index * page_size
        end = start + page_size
        page_messages = messages[start:end]

        page_data = {
            "page": page_index,
            "messages": page_messages,
        }

        page_path = pages_dir / f"page_{page_index:03d}.json"
        with page_path.open("w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

    # --- write meta ---
    meta = {
        "total_messages": total_messages,
        "page_size": page_size,
        "total_pages": total_pages,
        "order": "oldest_to_newest",
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    meta_path = output_dir / "meta.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Export completed")
    print(f"[INFO] Meta file: {meta_path}")
    print(f"[INFO] Pages directory: {pages_dir}")
