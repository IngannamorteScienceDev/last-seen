from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LastSeenConfig:
    encoding: str = "windows-1251"
    export_dir: Path = Path("export")
