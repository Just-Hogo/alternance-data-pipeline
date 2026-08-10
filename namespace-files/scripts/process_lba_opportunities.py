import json
import sys
from pathlib import Path


response_path = Path(sys.argv[1])
config_path = Path(sys.argv[2])
output_path = Path(sys.argv[3])

with config_path.open(encoding="utf-8") as file:
    config = json.load(file)

rome_codes = config["la_bonne_alternance"]["rome_codes"]

with response_path.open(encoding="utf-8") as file:
    data = json.load(file)

jobs = data.get("jobs", [])
recruiters = data.get("recruiters", [])
warnings = data.get("warnings", [])

print(f"{len(jobs)} offres récupérées")
print(f"{len(recruiters)} recruteurs potentiels")
print(f"Codes ROME configurés : {', '.join(rome_codes)}")

# La logique métier viendra ici :
# - validation de la réponse ;
# - normalisation des offres ;
# - filtrage des intitulés ;
# - déduplication ;
# - enregistrement en base.

result = {
    "jobs": jobs,
    "recruiters": recruiters,
    "warnings": warnings,
}

with output_path.open("w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)