"""
Last Seen — Media Downloader
----------------------------
Handles downloading media attachments from parsed messages.

Public API:
- download_dialog_media(messages, out_dir)
"""

from __future__ import annotations

import os
import hashlib
import requests
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse

from tqdm import tqdm


def _safe_filename(url: str) -> str:
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    if not name:
        name = hashlib.md5(url.encode()).hexdigest()
    return name


def _download_file(url: str, target: Path) -> bool:
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        with open(target, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception:
        return False


def download_dialog_media(
    messages: List[Dict[str, Any]],
    out_dir: str | Path = "export",
) -> int:
    """
    Download all media attachments referenced in messages.

    Adds local_path to attachment entries if downloaded.

    Returns:
        number of successfully downloaded files
    """
    out_dir = Path(out_dir)
    media_dir = out_dir / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    tasks = []

    for msg in messages:
        for att in msg.get("attachments", []):
            url = att.get("url")
            if not url:
                continue
            filename = _safe_filename(url)
            target = media_dir / filename
            tasks.append((url, target, att))

    if not tasks:
        print("[INFO] No media attachments found")
        return 0

    downloaded = 0

    for url, target, att in tqdm(
        tasks,
        desc="Downloading media",
        unit="file",
        dynamic_ncols=True,
    ):
        if target.exists():
            att["local_path"] = str(target)
            continue

        if _download_file(url, target):
            att["local_path"] = str(target)
            downloaded += 1

    print(f"[INFO] Downloaded {downloaded} new files")
    return downloaded
