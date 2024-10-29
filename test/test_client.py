import pytest
from sqlmodel import Session,select,create_engine,func
from ..server import client 
from ..server.models import Currency
from sqlalchemy import create_engine,select
from datetime import datetime

@pytest.fixture
def get_engine():
    return create_engine("sqlite:///../server/database.db",connect_args={"check_same_thread": False})

@pytest.fixture
def get_session(get_engine):
    with Session(get_engine) as session:
        yield session

@pytest.fixture
def get_client():
    return client


def test_get_story_price(get_client,get_session):
    test_ticker = "BTC"
    response = get_client.get_story_price(test_ticker)
    bd_records = get_session.exec(select(Currency).where(Currency.ticker==test_ticker)).all()

    assert response.status_code == 200

    assert len(response.json())==len(bd_records)

def test_get_curr_price(get_client,get_session):
    test_ticker = "ETH"
    response = get_client.get_curr_price(test_ticker)
    assert response.status_code == 200

    id_record = get_session.exec(select(func.max(Currency.id)).where(Currency.ticker==test_ticker)).all()

    assert response.json()["id"]==id_record[0][0] #id элемента совпало

def test_get_date_price(get_client,get_session):
    test_date = "2024-10-29"
    test_ticker = "BTC"

    response = get_client.get_date_price(test_ticker,test_date) 
    assert response.status_code == 200 #Проверить наличие записей в БД по этой дате

    date_obj = datetime.strptime(test_date, '%Y-%m-%d').date()

    bd_records = get_session.exec(
        select(Currency)
        .where(Currency.ticker==test_ticker)
        .where(Currency.date >= int(datetime.combine(date_obj, datetime.min.time()).timestamp()))
        .where(Currency.date < int(datetime.combine(date_obj, datetime.max.time()).timestamp()))
        .order_by(Currency.date.desc())
    ).all()

    assert len(response.json())==len(bd_records)#Кол-во записей совпало