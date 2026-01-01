import json
from pathlib import Path
from math import ceil

PAGE_SIZE = 100

def export_chunked(messages, export_dir: Path):
    export_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = export_dir / "pages"
    pages_dir.mkdir(exist_ok=True)

    total_messages = len(messages)
    total_pages = ceil(total_messages / PAGE_SIZE)

    date_index = {}

    for global_idx, msg in enumerate(messages):
        date = msg["datetime"].split("T")[0]

        if date not in date_index:
            page = global_idx // PAGE_SIZE
            offset = global_idx % PAGE_SIZE
            date_index[date] = {
                "page": page,
                "offset": offset
            }

    # write pages
    for page in range(total_pages):
        chunk = messages[
            page * PAGE_SIZE:(page + 1) * PAGE_SIZE
        ]
        with open(pages_dir / f"page_{page:03d}.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "page": page,
                    "messages": chunk
                },
                f,
                ensure_ascii=False,
                indent=2
            )

    # meta.json
    meta = {
        "total_pages": total_pages,
        "total_messages": total_messages,
        "page_size": PAGE_SIZE,
        "date_range": {
            "from": messages[0]["datetime"].split("T")[0],
            "to": messages[-1]["datetime"].split("T")[0],
        }
    }

    with open(export_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    with open(export_dir / "date_index.json", "w", encoding="utf-8") as f:
        json.dump(date_index, f, indent=2)

    print(f"[INFO] Exported {total_messages} messages")
    print(f"[INFO] Pages: {total_pages}")
    print(f"[INFO] Date index entries: {len(date_index)}")
