from fastapi import FastAPI,Query,Depends
from sqlmodel import create_engine,SQLModel,Session,select,func

engine=create_engine("sqlite:///./database.db",connect_args={"check_same_thread": False})  

from models import Currency
from typing import List
from datetime import datetime
import asyncio
import async_client 


def get_session():
    with Session(engine) as session:
        yield session


app= FastAPI()
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    asyncio.create_task(async_client.main())

    
@app.get("/currency",response_model=List[Currency])
async def get_story_price(
    ticker:str=Query(required = True,description="Enter currency name btc_usd or eth_usd"),
    session:Session = Depends(get_session)):
    response = session.exec(select(Currency).where(Currency.ticker==ticker)).all()

    print(f"Получение всех данных {ticker}:")
    for i in response:
        print(i)
    return response

@app.get("/currency/current",response_model=Currency)
async def get_curr_price(
    ticker:str=Query(required = True,description="Enter currency name btc_usd or eth_usd"),
    session:Session = Depends(get_session)):

    max_id = session.exec(select(func.max(Currency.id)).where(Currency.ticker==ticker)).all()
    max_id=int(max_id[0])
    response = session.exec(select(Currency).where(Currency.ticker==ticker).where(Currency.id==max_id)).all()

    print(f"Получение последних данных {ticker} : {response[0]}\n")
    return response[0]

@app.get("/currency/date",response_model=List[Currency])
async def get_date_price(
    ticker:str=Query(required = True,description="Enter currency name btc_usd or eth_usd"),
    date:str=Query(required = True,description="Enter date for sorting"),
    session:Session = Depends(get_session)):

    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return {"message": "Неверный формат даты. Используйте YYYY-MM-DD."}
    
    response = session.exec(
        select(Currency)
        .where(Currency.ticker==ticker)
        .where(Currency.date >= int(datetime.combine(date_obj, datetime.min.time()).timestamp()))
        .where(Currency.date < int(datetime.combine(date_obj, datetime.max.time()).timestamp()))
        .order_by(Currency.date.desc())
    ).all()
    print(f"Получение всех данных {ticker} по дате: {date} : ")
    if len(response):
        for i in response:
            print(i)
    else:
        print("Записей не найдено")
    return response

