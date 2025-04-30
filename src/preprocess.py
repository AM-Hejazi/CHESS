import os
from dotenv import load_dotenv

# Load environment variables for DeepSeek
load_dotenv(override=True)

# Initialize DeepSeek client
from deepseek import DeepSeekClient
from langchain.embeddings.base import Embeddings

# Fetch API key from env
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
if not deepseek_api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in environment")

# Initialize DeepSeek client instance
deepseek_client = DeepSeekClient(api_key=deepseek_api_key)

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
