import os
from typing import List, Dict
from src.domain.usecase.common.data_ingestion import AbstractDataIngestionCommon

class DataIngestionCommon(AbstractDataIngestionCommon):
    def read_folder(self, path: str) -> List[Dict[str, str]]:
        data: List[Dict[str, str]] = []

        if not os.path.isdir(path):
            print(f"Path não é uma pasta ou não existe: {path}")
            return data
        
        for title in os.listdir(path):
            arquivo = os.path.join(path, title)

            if os.path.isfile(arquivo):
                try:
                    with open(arquivo, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                except UnicodeDecodeError:
                    with open(arquivo, "r", encoding="latin-1") as f:
                        conteudo = f.read()

                data.append({
                    "title": title,
                    "content": conteudo
                })

        return data