import pickle
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from datasketch import MinHash, MinHashLSH

# ─── Helper: create a MinHash for a string ────────────────────────────────────
def _create_minhash(signature_size: int, string: str, n_gram: int) -> MinHash:
    """
    Creates a MinHash object for a given string.
    """
    m = MinHash(num_perm=signature_size)
    for i in range(len(string) - n_gram + 1):
        shard = string[i : i + n_gram]
        m.update(shard.encode("utf8"))
    return m


# ─── Loading the prebuilt LSH & MinHashes ─────────────────────────────────────
def load_db_lsh(db_directory_path: str) -> Tuple[MinHashLSH, Dict[str, Tuple[MinHash, str, str, str]]]:
    """
    Loads the LSH and MinHashes from the preprocessed files in the specified directory.
    """
    db_id = Path(db_directory_path).name
    preproc = Path(db_directory_path) / "preprocessed"

    # The LSH file:
    with open(preproc / f"{db_id}_lsh.pkl", "rb") as f:
        lsh = pickle.load(f)

    # Note: match the name used when persisting in preprocess.py:
    with open(preproc / f"{db_id}_minhash.pkl", "rb") as f:
        minhashes = pickle.load(f)

    return lsh, minhashes


# ─── Querying the LSH for similar values ──────────────────────────────────────
def _jaccard_similarity(m1: MinHash, m2: MinHash) -> float:
    """Jaccard similarity between two MinHashes."""
    return m1.jaccard(m2)

def query_lsh(
    lsh: MinHashLSH,
    minhashes: Dict[str, Tuple[MinHash, str, str, str]],
    keyword: str,
    signature_size: int = 100,
    n_gram: int = 3,
    top_n: int = 10
) -> Dict[str, Dict[str, List[str]]]:
    """
    Queries the LSH for similar values to the given keyword and returns the top results.
    """
    # 1) Build a MinHash for the query
    query_minhash = _create_minhash(signature_size, keyword, n_gram)

    # 2) Query the index
    results = lsh.query(query_minhash)

    # 3) Score & sort
    scored = [
        (key, _jaccard_similarity(query_minhash, minhashes[key][0]))
        for key in results
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    best = scored[:top_n]

    # 4) Collect by table→column
    out: Dict[str, Dict[str, List[str]]] = {}
    for key, score in best:
        _, table, column, value = minhashes[key]
        out.setdefault(table, {}).setdefault(column, []).append(value)

    return out
