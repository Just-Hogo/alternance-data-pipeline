import json
import os
import sys
from pathlib import Path


response_path = Path(sys.argv[1])

with response_path.open(encoding="utf-8") as file:
    data = json.load(file)

execution_id = os.environ["EXECUTION_ID"]
execution_date = os.environ["EXECUTION_DATE"]

output_path = Path(f"raw_{execution_date}_{execution_id}.json")

with output_path.open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)