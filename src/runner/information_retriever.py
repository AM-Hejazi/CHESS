import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load vector DB
def load_vector_db(tables_path, columns_path):
    tables_df = pd.read_csv(tables_path)
    tables_df['embedding'] = tables_df['embedding'].apply(lambda x: np.array(eval(x)))

    columns_df = pd.read_csv(columns_path)
    columns_df['embedding'] = columns_df['embedding'].apply(lambda x: np.array(eval(x)))

    return tables_df, columns_df

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Retrieve top-k similar items
def retrieve_similar_items(query: str, top_k=5, target='tables', tables_df=None, columns_df=None):
    query_embedding = model.encode([query], normalize_embeddings=True)

    if target == 'tables':
        data = tables_df
    elif target == 'columns':
        data = columns_df
    else:
        raise ValueError("Target must be 'tables' or 'columns'")

    embeddings = np.vstack(data['embedding'].to_numpy())
    scores = cosine_similarity(embeddings, query_embedding).flatten()

    top_indices = scores.argsort()[::-1][:top_k]
    results = data.iloc[top_indices]

    return results[['id', 'text']], scores[top_indices]
