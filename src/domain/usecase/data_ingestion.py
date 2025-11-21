from pathlib import Path
from dataclasses import dataclass
from src.pkg.util.share import generate_uuid
from src.domain.usecase.common.data_ingestion import AbstractDataIngestionCommon
from src.domain.usecase.transformer.data_ingestion import AbstractDataIngestionTransformer
from src.domain.usecase.embedding.data_ingestion import AbstractDataIngestionEmbedding
from src.domain.usecase.repository.data_ingestion import AbstractDataIngestionRepository

@dataclass
class DataIngestionUseCase:
    data_ingestion_common: AbstractDataIngestionCommon
    data_ingestion_transformer: AbstractDataIngestionTransformer
    data_ingestion_embedding: AbstractDataIngestionEmbedding
    data_ingestion_repository: AbstractDataIngestionRepository

    async def execute(self):
        try:
            root = Path.cwd()
            path = root / "data"

            data = self.data_ingestion_common.read_folder(path=path)

            for item in data:
                title = item["title"]
                content = item["content"]

                chunks = self.data_ingestion_transformer.generate_chunks(full_text=content)

                for chunk in chunks:
                    payload = {
                        "title": title,
                        "text": chunk
                    }
                    
                    vector = self.data_ingestion_embedding.generate_vector(target=chunk)

                    vector_id = generate_uuid()

                    await self.data_ingestion_repository.insert(vector_id=vector_id, payload=payload, vector=vector)

                pass
        except Exception as e:
            raise e