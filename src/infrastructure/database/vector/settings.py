from qdrant_client import QdrantClient
from pydantic_settings import BaseSettings
from qdrant_client.models import VectorParams, Distance

class VectorStorageSettings(BaseSettings):
    def connect(self) -> QdrantClient:
        """
        Cria e retorna uma instância do QdrantClient conectada ao endereço configurado.
        """
        client = QdrantClient(url="127.0.0.1:6333")
        return client

vectorStorageSettings = VectorStorageSettings()

client = vectorStorageSettings.connect()

client.recreate_collection(
    collection_name="data",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)