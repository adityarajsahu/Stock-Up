import sqlite3
import pandas as pd
import sqlalchemy
import schedule
import time
from datetime import date, timedelta
import datetime
import yfinance as yf
import uuid

engine = sqlalchemy.create_engine('sqlite:///stocks.db')

symbols = ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'META', 'GOOGL', 'NVDA', 'NIO', 'AMD', 'MA', 'BABA', 'PFE', 'KO', 'SHOP', 'PEP', 'TM', 'AZ', 'ORCL']

def updateDB():
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        today = date.today()
        df = ticker.history(start = today, end = today, actions = False, rounding = True)
        df = df.drop(columns=['Volume', 'Open'])
        df['DATE'] = today.strftime('%d/%m/%Y')
        df['STOCK NAME'] = ticker.info['longName']
        df['SYMBOL'] = symbol
        df['id'] = uuid.uuid1()
        df = df.set_index('id')
        df.to_sql(symbol, engine, if_exists='append', index = False)
        print("New record added to {} table".format(symbol))