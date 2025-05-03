import os
import pickle
import logging
from pathlib import Path

from datasketch import MinHash, MinHashLSH
from tqdm import tqdm
from dotenv import load_dotenv

from runner.database_manager import DatabaseManager
from database_utils.db_info import get_db_all_tables, get_table_all_columns

# ── Load env & globals ────────────────────────────────────────────────────────
load_dotenv(override=True)
DB_MODE = os.getenv("DATA_MODE", "prod")
DB_ID   = os.getenv("DB_NAME")


def _create_minhash(signature_size: int, string: str, n_gram: int) -> MinHash:
    """
    Creates a MinHash object for a given string.
    """
    m = MinHash(num_perm=signature_size)
    for i in range(len(string) - n_gram + 1):
        shard = string[i : i + n_gram]
        m.update(shard.encode("utf8"))
    return m


def make_db_lsh(
    db_root: str,
    *,
    signature_size: int,
    n_gram: int,
    threshold: float,
    verbose: bool,
):
    """
    Build a MinHash LSH index directly from SQL Server, handling schema-qualified names.
    """
    logging.info(f"Creating LSH for {DB_ID} via direct DB queries")
    dm = DatabaseManager(DB_MODE, DB_ID)

    all_values = []
    for full_tbl in ["Wamas.ART"]: #***get_db_all_tables():
        # full_tbl might be "dbo.MyTable" or just "MyTable"
        if "." in full_tbl:
            schema, table = full_tbl.split(".", 1)
            qualified = f"[{schema}].[{table}]"
        else:
            qualified = f"[{full_tbl}]"

        for col in get_table_all_columns(table_name=full_tbl):
            try:
                rows = dm.fetch_all(
                    f"SELECT DISTINCT [{col}] FROM {qualified} WHERE [{col}] IS NOT NULL;"
                )
                all_values.extend(r[0] for r in rows if r[0] is not None)
            except Exception as e:
                logging.warning(f"Skipping {full_tbl}.{col}: {e}")

    logging.info(f"Total unique values fetched: {len(all_values)}")

    # 3) Build the LSH index
    lsh = MinHashLSH(threshold=threshold, num_perm=signature_size)
    minhashes = {}
    progress = tqdm(total=len(all_values), desc="Creating LSH") if verbose else None

    for idx, val in enumerate(all_values):
        m = _create_minhash(signature_size, str(val), n_gram)
        key = f"{DB_ID}_{idx}"
        lsh.insert(key, m)
        minhashes[key] = (m, None, None, val)
        if progress:
            progress.update(1)

    if progress:
        progress.close()

    # 4) Persist artifacts
    out_dir = Path(db_root) / DB_ID / "preprocessed"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / f"{DB_ID}_lsh.pkl", "wb") as f:
        pickle.dump(lsh, f)
    with open(out_dir / f"{DB_ID}_minhash.pkl", "wb") as f:
        pickle.dump(minhashes, f)

    logging.info(f"LSH for {DB_ID} created and saved at {out_dir}")
