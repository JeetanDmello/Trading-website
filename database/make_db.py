# Importing all the necessary libraries
import mysql.connector
import pandas as pd
import time
import datetime


# Initializing and connecting to MYSQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)

# Initializing the cursor.
cursor = db.cursor()

# Getting all the Data from stocks table for its tickers 
cursor.execute("SELECT * FROM stocks;")
tickers = [tup[0] for tup in cursor.fetchall()]

# Getting the stock_data for each ticker in tickers.
for ticker in tickers:

    #Setting the time interval from when the prices are required.
    interval = '1d'
    period1 = int(time.mktime(datetime.datetime(2015, 1, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime.now().timetuple()))

    #calling the yahoo api to get stock_data from each ticker
    print(f"{ticker}")
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    df = pd.read_csv(query_string)

    #storing the stock data appropirately in a csv file
    df["stock_id"] = [ticker for _ in range(df.shape[0])]
    df = df.iloc[:, [7, 0, 1, 2, 3, 4, 6]]
    df.to_csv("db_files/stock_data" + '.csv', mode='a', index=False, header=False)

# reading the .csv file that has stock_data for all tickers
df_stockdata = pd.read_csv("db_files/stock_data.csv", low_memory=False, header=None).dropna()

# Storing the whole csv file in the database
# Have done this because date and stock_id can be taken into the db in a certain format only.
for i in range(df_stockdata.shape[0]):
    stock_data = [df_stockdata.iloc[i][col] for col in range(df_stockdata.shape[1])]
    if all(stock_data):
        print(f"{i} done")
        cursor.execute("""INSERT INTO stock_data (stock_id, datetime, open, high, low, close, volume)
VALUES ("{}",DATE '{}',{},{},{},{},{});""".format(stock_data[0], stock_data[1], stock_data[2], stock_data[3],stock_data[4], stock_data[5], stock_data[6]))

# Commit the changes to the database and close it

db.commit()
db.close()