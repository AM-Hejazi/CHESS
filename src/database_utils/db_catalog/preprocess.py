import os
from dotenv import load_dotenv

# Load environment variables for DeepSeek
load_dotenv(override=True)

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
if not deepseek_api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in environment")

# Use the DeepSeekAPI client from the deepseek package
from deepseek import DeepSeekAPI

deepseek_client = DeepSeekAPI(api_key=deepseek_api_key)

# LangChain-compatible embeddings interface
from langchain.embeddings.base import Embeddings

class DeepSeekEmbeddings(Embeddings):
    def __init__(self, client: DeepSeekAPI):
        self.client = client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.client.embed_query(text)

# Export the embedding function for CHESS
EMBEDDING_FUNCTION = DeepSeekEmbeddings(deepseek_client)
