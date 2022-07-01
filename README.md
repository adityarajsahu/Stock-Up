# Stock-Up

This repository contains code for storing stock data of provided companies in a SQLite database and provides an API for access information about top 10 gainers, top 10 losers and weekly report.


## How to run the app locally?

First, install all dependencies
```
pip install -r requirements.txt
```

Next, run the app.py Python file
```
python app.py
```

## My Approach to the Problem

### Inserting stock records into Database
1. Created a SQLite Database using **SQLAlchemy**.
2. Using **yfinance** python package, I downloaded the stock price for current date in form of a Pandas dataframe. Then, I removed Volume and Open columns from the dataframe.
3. Then, I added date, stock name, symbol and id into the dataframe. For generating id, I used **uuid** python package.
4. Then, I inserted the dataframe into the database.

### Creating the API
1. I created a Flask app for API.
2. Using **schedule** python package, I scheduled the updation of database everyday at 18:00 IST. In this step, new record will be added for the current day stock prices.
3. For finding the top gainers, I calculated the change percentage in the closing prices of the previous day and current day. Then, I stored the symbol and change percentage in dict and appended it to a list. After that, I sorted the list in decreasing order and returned the first 10 elements of the list 
4. For finding the top losers, the process was same as that of top gainers, but the list was sorted in ascending order.
5. For the weekly report, the max value of High column, min value of Low column and mean value of Close column was calculated and returned.

## Problems Encountered

I faced difficulty in downloading data and inserting it into the database. Initially, I had tried downloading data from and Yahoo Finance API, but the API key changes everyday. It is not a good practice to manually change the API key and I don't know if there is a way to update it automatically. 

## How the application can be improved

