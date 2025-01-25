import bs4
import requests
import pandas as pd
from sqlmodel import Field, Session, SQLModel, create_engine, select
from dotenv import dotenv_values
from fastapi import Depends

config = dotenv_values()

engine = create_engine(f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASS']}@127.0.0.1:5432/stockdata")

class Symbols(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str = Field(index=True)
    name: str = Field(default=None)
    sector: str = Field(default=None)
        

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
source = requests.get(url)

soup = bs4.BeautifulSoup(source.content, 'lxml')
data = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

df = pd.DataFrame(data, columns=['symbol', 'name', 'sector', 'subindustry', 'city', 'state', 'cik', 'founded'])
new_df = df[['symbol', 'name', 'sector']]

        
new_df.to_sql(con=engine, name='Symbols')

print("Stock symbols added to database")


