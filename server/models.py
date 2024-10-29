from sqlmodel import SQLModel,Field
from datetime import datetime

class Currency(SQLModel,table= True):
    id:int=Field(primary_key=True)
    ticker:str
    price:float
    date:int = Field(default_factory=lambda:
    int(datetime.now().timestamp()))
