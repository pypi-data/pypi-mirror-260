"""Configuration file for the project."""

from pathlib import Path


class Config:
    """Configuration class for the project."""

    root_dir: Path = Path(__file__).resolve().parent
    prompt_dir: Path = root_dir / "prompts"


config = Config()
