CREATE TABLE user ( user_id INTEGER,
                    username VARCHAR(20) NOT NULL UNIQUE,
                    user_password VARCHAR(20)NOT NULL,
                    account_no VARCHAR(20),
                    balance INTEGER,
                    email VARCHAR(60) NOT NULL UNIQUE,
                    PRIMARY KEY (user_id));

CREATE TABLE admin ( admin_id INTEGER NOT NULL UNIQUE,
                    admin_password VARCHAR(20) NOT NULL,
                    PRIMARY KEY (admin_id));

CREATE TABLE stocks(  stock_id VARCHAR(10) NOT NULL UNIQUE,
                      company_name VARCHAR(100) NOT NULL);

CREATE TABLE payment_info ( payment_id INTEGER NOT NULL UNIQUE,
                    user_id INTEGER NOT NULL UNIQUE,
                    amount INTEGER,
                    date DATETIME,
                    PRIMARY KEY (payment_id),
                    FOREIGN KEY (user_id) REFERENCES user(user_id));

CREATE TABLE  feedback ( user_id INTEGER NOT NULL,
                    admin_id INTEGER NOT NULL,
                    feedback VARCHAR(200),
                    response VARCHAR(200),
                    FOREIGN KEY (user_id) REFERENCES user(user_id),
                    FOREIGN KEY (admin_id) REFERENCES admin(admin_id));

CREATE TABLE buy_stocks( user_id INTEGER NOT NULL,
                         stock_id VARCHAR(10) NOT NULL,
                         volume INTEGER NOT NULL,
                         price INTEGER NOT NULL,
                         datetime DATETIME NOT NULL,
                         PRIMARY KEY (user_id, stock_id),
                         FOREIGN KEY (user_id) REFERENCES user(user_id),
                         FOREIGN KEY (stock_id) REFERENCES stocks(stock_id));

CREATE TABLE sell_stocks( user_id INTEGER NOT NULL,
                         stock_id VARCHAR(10) NOT NULL,
                         volume INTEGER NOT NULL,
                         price INTEGER NOT NULL,
                         datetime DATETIME NOT NULL,
                         PRIMARY KEY (user_id, stock_id),
                         FOREIGN KEY (user_id) REFERENCES user(user_id),
                         FOREIGN KEY (stock_id) REFERENCES stocks(stock_id));

CREATE TABLE stock_data (stock_id VARCHAR(10) NOT NULL,
                         datetime DATETIME NOT NULL,
                         open float NOT NULL,
                         high FLOAT NOT NULL,
                         low FLOAT NOT NULL,
                         close FLOAT NOT NULL,
                         volume FLOAT NOT NULL, 
                         FOREIGN KEY (stock_id) REFERENCES stocks(stock_id));


-- INSERT INTO stock_data (stock_id, datetime, open, high, low, close, volume)
-- VALUES ("ACC.NS",DATE '2015-01-02',1406.400024,1431.0,1405.550049,1425.900024,153349.0);





