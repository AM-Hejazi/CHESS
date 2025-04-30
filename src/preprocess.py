import os
from dotenv import load_dotenv

# Load environment variables for DeepSeek
def load_api_key():
    load_dotenv(override=True)
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment")
    return key

# Initialize DeepSeek client
from deepseek import DeepSeekClient
from langchain.embeddings.base import Embeddings

# Fetch and validate API key
from dotenv import load_dotenv
api_key = load_api_key()

deepseek_client = DeepSeekClient(api_key=api_key)

# Define LangChain-compatible embeddings wrapper using DeepSeek
class DeepSeekEmbeddings(Embeddings):
    def __init__(self, client: DeepSeekClient):
        self.client = client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.client.embed_query(text)

# Set EMBEDDING_FUNCTION to use the DeepSeekEmbeddings
EMBEDDING_FUNCTION = DeepSeekEmbeddings(deepseek_client)
