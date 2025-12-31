"""
Media downloader (placeholder).

Later this will download files for attachments where downloadable=True.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Dict


def download_media(attachments: Iterable[Dict], output_dir: Path) -> None:
    """
    Placeholder downloader.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    # TODO: implement downloading with requests + hashing + dedupe
    return
