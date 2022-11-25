# Importing all the necessary libraries
import mysql.connector
import pandas as pd
import time
import datetime
import os

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)

cursor = db.cursor()
cursor.execute("use db")

cursor.execute("SELECT * FROM stocks;")
tickers = [tup[0] for tup in cursor.fetchall()]

cursor.execute("SELECT datetime FROM stock_data;")
latest_date = max(cursor.fetchall())[0] + datetime.timedelta(days=1)
current_date = datetime.date.today() - datetime.timedelta(days=2)

df = pd.DataFrame()
if current_date != latest_date:
    for ticker in tickers:
        interval = '1d'
        period1 = int(time.mktime(latest_date.timetuple()))
        period2 = int(time.mktime(current_date.timetuple()))

        print(f"{ticker}")
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        df["stock_id"] = [ticker for _ in range(df.shape[0])]
        df = df.iloc[:, [7, 0, 1, 2, 3, 4, 6]]
        df.to_csv("db_files/updated_stock_prices.csv", mode='a', index=False, header=False)

file_path = 'db_files/updated_stock_prices.csv'
# check if size of file is 0
if os.stat(file_path).st_size == 0:
    print('File is empty')
    df_stockdata = pd.DataFrame()
else:
    df_stockdata = pd.read_csv("db_files/updated_stock_prices.csv", low_memory=False, header=None).dropna()
    df_stockdata

for i in range(df_stockdata.shape[0]):
    stock_data = [df_stockdata.iloc[i][col] for col in range(df_stockdata.shape[1])]
    if all(stock_data):
        print(f"{i} done")
        cursor.execute("""INSERT INTO stock_data (stock_id, datetime, open, high, low, close, volume)
VALUES ("{}",DATE '{}',{},{},{},{},{});""".format(stock_data[0], stock_data[1], stock_data[2], stock_data[3],stock_data[4], stock_data[5], stock_data[6]))

db.commit()
db.close()