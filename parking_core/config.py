"""Load a city configuration. The core never hard-codes city values."""
from pathlib import Path

import yaml

CITIES_DIR = Path(__file__).resolve().parent.parent / "cities"


def load_city(city_id: str, cities_dir: Path = CITIES_DIR) -> dict:
    path = cities_dir / city_id / "city.yaml"
    with open(path, encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if config.get("id") != city_id:
        raise ValueError(f"{path}: id does not match directory name")
    return config
