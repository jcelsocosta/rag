from pydantic import BaseModel

class SearchApplicationInput(BaseModel):
    message: str
