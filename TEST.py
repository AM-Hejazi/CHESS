#!/usr/bin/env python3
import os, sys, json
from pathlib import Path
from dotenv import load_dotenv

# 1) add src/ to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT/"src"))

# 2) load env and get schema
load_dotenv(override=True)
db_name = os.getenv("DB_NAME", "DataWarehouse")

from database_utils.db_info import get_db_schema

schema = get_db_schema()   # -> Dict[str,List[str]]

# 3) write it out
out_dir = ROOT/"preprocessed_artifacts"/db_name
out_dir.mkdir(parents=True, exist_ok=True)
with open(out_dir/"schema.json","w", encoding="utf8") as f:
    json.dump(schema, f, indent=2)

print(f"✅ Wrote {len(schema)} tables to {out_dir/'schema.json'}")
