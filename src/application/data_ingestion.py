from src.domain import data_ingestion_usecase

async def initialize_data_ingestion():
    await data_ingestion_usecase.execute()