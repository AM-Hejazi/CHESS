import os
import logging
import numpy as np
from typing import List, Dict

from database_utils.db_catalog.preprocess import EMBEDDING_FUNCTION

def _load_vectors(csv_name: str):
    """
    Helper to load a vector CSV only if it exists.
    Returns a tuple (ids, vectors) or ([], []) if missing.
    """
    try:
        import pandas as pd
    except ImportError:
        logging.warning("pandas not installed—vector search disabled.")
        return [], []

    base = os.getenv("DB_ROOT_DIRECTORY", "./data/dev/dev_databases")
    vdb  = os.path.join(base, os.getenv("DB_NAME"), "vector_db")
    path = os.path.join(vdb, csv_name)
    if not os.path.exists(path):
        logging.warning(f"{csv_name} not found at {path}—vector search disabled.")
        return [], []

    df = pd.read_csv(path)
    ids = df.iloc[:, 0].tolist()  # adjust if your id column differs
    # assume the last column is the vector string "[x, y, z]"
    raw = df.iloc[:, -1].tolist()
    vectors = []
    for s in raw:
        arr = np.fromstring(s.strip("[]"), sep=",")
        vectors.append(arr)
    return ids, vectors

def query_vector_db(question: str, k: int = 10) -> List[Dict]:
    """
    Compute query embedding and rank the precomputed table vectors.
    """
    table_ids, table_vecs = _load_vectors("tables_vector_db.csv")
    if not table_vecs:
        return []

    qv = np.array(EMBEDDING_FUNCTION.embed_query(question), dtype=float)
    # cosine similarity
    sims = [float(np.dot(v, qv) / (np.linalg.norm(v)*np.linalg.norm(qv) + 1e-10))
            for v in table_vecs]
    # get top k
    idxs = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:k]

    results = []
    # reload pandas to get full metadata
    import pandas as pd
    df = pd.read_csv(os.path.join(os.getenv("DB_ROOT_DIRECTORY"),
                                  os.getenv("DB_NAME"),
                                  "vector_db",
                                  "tables_vector_db.csv"))
    for i in idxs:
        row = df.iloc[i].to_dict()
        # remove the raw vector column if you like
        row.pop("vector", None)
        results.append(row)
    return results
