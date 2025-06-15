# managing reading and writing to a file

import json
from typing import List
from pathlib import Path

data_path = Path("data/data.json")
data_path.parent.mkdir(exist_ok=True)

def load_data() -> List[dict]:
    if data_path.exists():
        with open(data_path, "r") as f:
            return json.load(f)
    return []

def save_data(data: List[dict]):
    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)


