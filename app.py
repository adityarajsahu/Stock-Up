from flask import Flask, jsonify
import sqlite3
import sqlalchemy
import pandas as pd
from main import updateDB
import time
import schedule
app = Flask(__name__)

engine = sqlalchemy.create_engine('sqlite:///stocks.db')

symbols = ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'META', 'GOOGL', 'NVDA', 'NIO', 'AMD', 'MA', 'BABA', 'PFE', 'KO', 'SHOP', 'PEP', 'TM', 'AZ', 'ORCL']

schedule.every().day.at("18:00").do(updateDB)

while True:
    schedule.run_pending()
    time.sleep(1)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get_top_gainers')
def find_top_gainers():
    list_of_dict = []
    for symbol in symbols:
        df = pd.read_sql(symbol, engine)
        change_percent = ((df['Close'][df.shape[0] - 1]) - (df['Close'][df.shape[0] - 2])) / (df['Close'][df.shape[0] - 2])
        list_of_dict.append({'rank': 0, ticker': symbol, 'change_percent': change_percent})
    
    new_list = sorted(list_of_dict, key = lambda d: d['change_percent'], reverse=True)

    i = 1
    for elem in new_list:
        elem['rank'] = 1
        i = i + 1
    
    return new_list[:10]

@app.route('/get_top_losers')
def find_top_losers():
    list_of_dict = []
    for symbol in symbols:
        df = pd.read_sql(symbol, engine)
        change_percent = ((df['Close'][df.shape[0] - 1]) - (df['Close'][df.shape[0] - 2])) / (df['Close'][df.shape[0] - 2])
        list_of_dict.append({'rank': 0, ticker': symbol, 'change_percent': change_percent})
    
    new_list = sorted(list_of_dict, key = lambda d: d['change_percent'])

    i = 1
    for elem in new_list:
        elem['rank'] = 1
        i = i + 1
    
    return new_list[:10]

@app.route('/generate_weekly_report')
def find_weekly_report():
    list_of_dict = []
    for symbol in symbols:
        df = pd.read_sql(symbol, engine)
        highest = 0
        lowest = 0
        avg = 0
        if(df.shape[0] < 7):
            highest = df['High'].max()
            lowest = df['Low'].min()
            avg = df['Close'].mean()

        new_df = df.iloc[-7:]
        highest = new_df['High'].max()
        lowest = new_df['Low'].min()
        avg = new_df['Close'].mean()

        list_of_dict.append({'ticker': symbol, 'high': highest, 'low': lowest, 'average': avg})
    
    return list_of_dict

if __name__ == "__main__":
    app.run(debug=True)