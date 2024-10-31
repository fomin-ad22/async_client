import asyncio
import aiohttp
from sqlmodel import Session
from main import engine
from models import Currency

async def fetch_currency_data(session:aiohttp.ClientSession,ticker:str)->dict:
    url=f"https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency={ticker}&kind=future"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            # возьмем среднюю цену между бидом и аском
            bid = float(data["result"][0]["bid_price"])
            ask = float(data["result"][0]["ask_price"])
            average_price = (bid+ask)/2
            return {"ticker":ticker,"price":average_price}
        else:
            print(f"Ошибка при получении данных для {ticker}: {response.status}")
            return None

async def update_currency_database(session: aiohttp.ClientSession):
  with Session(engine) as db:

    btc_data = await fetch_currency_data(session, "BTC")
    eth_data = await fetch_currency_data(session, "ETH")

    if btc_data and eth_data:
      for data in [btc_data, eth_data]:
        db.add(Currency(ticker=data["ticker"],price=float('{:.2f}'.format(data["price"]))))
        db.commit()


async def main():
    async with aiohttp.ClientSession() as session:
      while True:
        await update_currency_database(session)
        await asyncio.sleep(60)

if __name__ =="__main__":
  print("Run")
  asyncio.run(main())
    
