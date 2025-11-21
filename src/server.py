import asyncio
import uvicorn
from fastapi import FastAPI
from src.application.router import router
from src.application.data_ingestion import initialize_data_ingestion

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_tasks():
    print("Inicializando a aplicação")
    print("Inicializando a ingestão de dados")
    await initialize_data_ingestion()

def main():
    uvicorn.run("src.server:app", host="0.0.0.0", port=3035, reload=False)

if __name__ == "__main__":
    main()