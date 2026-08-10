import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Modules personnels
from lba.transformations import transform_job

# Paramètre récupérés.
response_path = Path(sys.argv[1])
config_path = Path(sys.argv[2])
output_path = Path(sys.argv[3])

with config_path.open(encoding="utf-8") as file:
    config = json.load(file)

lba_config = config["la_bonne_alternance"]
rome_codes = lba_config["rome_codes"]
max_offer_age_hours = lba_config.get("max_offer_age_hours", 24)

with response_path.open(encoding="utf-8") as file:
    data = json.load(file)

jobs = data.get("jobs", [])
warnings = data.get("warnings", [])

now = datetime.now(timezone.utc)
minimum_creation_date = now - timedelta(hours=max_offer_age_hours)

recent_jobs = []

for job in jobs:
    creation_value = (
        job.get("offer", {})
        .get("publication", {})
        .get("creation")
    )

    if creation_value is None:
        continue

    creation_date = datetime.fromisoformat(
        creation_value.replace("Z", "+00:00")
    )

    if creation_date.tzinfo is None:
        creation_date = creation_date.replace(tzinfo=timezone.utc)

    if minimum_creation_date <= creation_date <= now:
        recent_jobs.append(job)

print(f"{len(jobs)} offres récupérées")
print(
    f"{len(recent_jobs)} offres publiées "
    f"depuis moins de {max_offer_age_hours} heures"
)

result = {
    "jobs": recent_jobs,
    "warnings": warnings,
}

with output_path.open("w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)