import os
import chromadb
from dotenv import load_dotenv

# Load environment variables (including DEEPSEEK_API_KEY)
load_dotenv(override=True)

# Initialize DeepSeek client
from deepseek import DeepSeekClient

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
if not deepseek_api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in environment")

deepseek_client = DeepSeekClient(api_key=deepseek_api_key)

# Define a LangChain–compatible embeddings wrapper using DeepSeek
from langchain.embeddings.base import Embeddings

class DeepSeekEmbeddings(Embeddings):
    def __init__(self, client: DeepSeekClient):
        self.client = client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.client.embed_query(text)

# Use DeepSeekEmbeddings instead of OpenAIEmbeddings
EMBEDDING_FUNCTION = DeepSeekEmbeddings(deepseek_client)
