from __future__ import annotations

import logging
import hashlib
from pathlib import Path
from typing import Iterable, Dict
from urllib.parse import urlparse

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)

TIMEOUT = 15


def _hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def _get_extension(url: str) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix
    return suffix if suffix else ""


def _target_subdir(att_type: str) -> str:
    if att_type == "photo":
        return "photo"
    if att_type == "voice_message":
        return "voice"
    return "files"


def download_media(
    messages: Iterable[Dict],
    media_root: Path,
) -> int:
    """
    Download all downloadable attachments from messages.
    Updates attachments in-place with local_path.
    """
    media_root.mkdir(parents=True, exist_ok=True)

    attachments = []
    for msg in messages:
        for att in msg.get("attachments", []):
            if att.get("downloadable") and att.get("source_url"):
                attachments.append(att)

    if not attachments:
        logger.info("No downloadable attachments found")
        return 0

    logger.info(f"Downloading {len(attachments)} attachments")

    downloaded = 0

    for att in tqdm(attachments, desc="Downloading media", unit="file"):
        url = att["source_url"]
        att_type = att["type"]

        subdir = _target_subdir(att_type)
        target_dir = media_root / subdir
        target_dir.mkdir(parents=True, exist_ok=True)

        file_hash = _hash_url(url)
        ext = _get_extension(url)
        target_path = target_dir / f"{file_hash}{ext}"

        # Skip if already downloaded
        if target_path.exists():
            att["local_path"] = str(target_path)
            continue

        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            with open(target_path, "wb") as f:
                f.write(response.content)

            att["local_path"] = str(target_path)
            downloaded += 1

        except Exception as e:
            logger.warning(f"Failed to download {url}: {e}")

    logger.info(f"Downloaded {downloaded} new files")
    return downloaded
