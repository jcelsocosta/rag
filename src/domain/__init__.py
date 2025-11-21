from src.infrastructure.database.vector.repository.search import SearchRepository
from src.domain.usecase.search import SearchUseCase
from src.infrastructure.embedding.search import SearchEmbedding
from src.infrastructure.guardrails.search import SearchGuardrails
from src.domain.usecase.data_ingestion import DataIngestionUseCase
from src.infrastructure.common.data_ingestion import DataIngestionCommon
from src.infrastructure.embedding.data_ingestion import DataIngestionEmbedding
from src.infrastructure.database.vector.repository.data_ingestion import DataIngestionRepository
from src.infrastructure.transformer.data_ingestion import DataIngestionTransformer

search_repository = SearchRepository()
search_embedding  = SearchEmbedding()
search_guardrails = SearchGuardrails()

search_use_case = SearchUseCase(
    search_repository=search_repository,
    search_embedding=search_embedding,
    search_guardrails=search_guardrails
)

data_ingestion_common = DataIngestionCommon()
data_ingestion_embedding = DataIngestionEmbedding()
data_ingestion_repository = DataIngestionRepository()
data_ingestion_transformer = DataIngestionTransformer()

data_ingestion_usecase = DataIngestionUseCase(
    data_ingestion_common=data_ingestion_common,
    data_ingestion_embedding=data_ingestion_embedding,
    data_ingestion_repository=data_ingestion_repository,
    data_ingestion_transformer=data_ingestion_transformer
)

__all__ = ["search_use_case", "data_ingestion_usecase"]