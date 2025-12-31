import logging
from pathlib import Path
from typing import Iterable, Dict

from tqdm import tqdm

logger = logging.getLogger(__name__)


def download_media(attachments: Iterable[Dict], output_dir: Path) -> None:
    downloadable = [a for a in attachments if a.get("downloadable")]

    if not downloadable:
        logger.info("No downloadable attachments found")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading {len(downloadable)} attachments")

    for att in tqdm(downloadable, desc="Downloading media", unit="file"):
        logger.info(f"Would download: {att['source_url']}")
