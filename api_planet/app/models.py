#Data format models that API will use for validation
from pydantic import BaseModel

class Mosaic(BaseModel):
    mosaic_name:str

