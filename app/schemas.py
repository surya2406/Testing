from pydantic import BaseModel

class Products(BaseModel):
    name:str
    sales:str