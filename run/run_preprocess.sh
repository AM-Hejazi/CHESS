#!/usr/bin/env bash

# 1) load your .env (DB creds, DEEPSEEK key, etc.)
set -o allexport
source .env
set +o allexport

# 2) where do we dump the artifacts?
db_root_directory="./preprocessed_artifacts"

# 3) which database are we targeting?
#    if your script only supports 'all', leave it.
#    Otherwise you can pass your actual DB_NAME (from .env)
db_id="${DB_NAME:-all}"

# 4) tuning parameters for the MinHash / vector ingestion
signature_size=100
n_gram=3
threshold=0.01
verbose=true

# 5) invoke the Python entrypoint
python3 -u ./src/preprocess.py \
    --db_root_directory "${db_root_directory}" \
    --signature_size   "${signature_size}"   \
    --n_gram           "${n_gram}"           \
    --threshold        "${threshold}"        \
    --db_id            "${db_id}"            \
    --verbose          "${verbose}"
