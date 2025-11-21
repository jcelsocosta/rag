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
    print("Aguardando 30 segundos para o Qdrant iniciar...")
    await asyncio.sleep(30)

    print("Inicializando a ingestão de dados")
    await initialize_data_ingestion()

def main():
    uvicorn.run("src.server:app", host="0.0.0.0", port=8080, reload=False)

if __name__ == "__main__":
    main()