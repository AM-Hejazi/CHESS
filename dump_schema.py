#!/usr/bin/env python3
"""
dump_schema.py

Connects to your SQL Server (via Windows auth) and writes out
preprocessed_artifacts/<DB_NAME>/schema.json
"""

import sys
from pathlib import Path

# 1) Compute paths
PROJECT_ROOT = Path(__file__).parent
SRC_ROOT     = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

# 2) Add src/ (not CHESS/) to PYTHONPATH
sys.path.insert(0, str(SRC_ROOT))

import os
from dotenv import load_dotenv

# 1) Load your .env
load_dotenv(override=True)

# 2) Grab mode and DB name
MODE  = os.getenv("DATA_MODE", "prod")
DB_ID = os.getenv("DB_NAME")

# 3) Ensure the output folder exists
OUT_ROOT = Path("preprocessed_artifacts") / DB_ID
OUT_ROOT.mkdir(parents=True, exist_ok=True)

# 4) Import and run the schema generator
from runner.database_manager import DatabaseManager
from database_utils.schema_generator import DatabaseSchemaGenerator

# Initialize the manager & generator
dm  = DatabaseManager(MODE, DB_ID)
gen = DatabaseSchemaGenerator(dm, str(OUT_ROOT))

# Dump only the schema (table→[columns])
gen.dump_schema()

print(f"✅ Wrote schema.json to {OUT_ROOT / 'schema.json'}")
