import json
import logging
from pathlib import Path
from typing import List, Dict

from tqdm import tqdm

logger = logging.getLogger(__name__)


def export_messages_to_json(
    messages: List[Dict],
    output_path: Path
) -> None:
    """
    Export parsed messages to JSON file.
    """
    logger.info(f"Exporting {len(messages)} messages to {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            messages,
            f,
            ensure_ascii=False,
            indent=2
        )

    logger.info("Export completed successfully")
