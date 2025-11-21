from src.domain.usecase.embedding.data_ingestion import AbstractDataIngestionEmbedding
from typing import List
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(MODEL_NAME)

class DataIngestionEmbedding(AbstractDataIngestionEmbedding):
    def generate_vector(self, target: str) -> List[float]:
        target_embedding = model.encode(target, normalize_embeddings=True, convert_to_numpy=True)

        return target_embedding