#Data format models that API will use for validation
from pydantic import BaseModel
from typing import List

class Mosaic(BaseModel):
    mosaic_name:str



