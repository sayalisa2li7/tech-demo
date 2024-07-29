import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = 'mysql+pymysql://sayali97:Sugandha1274*@localhost:3306/stock_data'

engine = create_engine(DATABASE_URL)

def get_daily_closing_prices():
    query = """
    SELECT date, ticker, close
    FROM stock_prices_data
    WHERE date = CURRENT_DATE
    """
    df = pd.read_sql(query, engine)
    return df

def get_price_change_percentage(period):
    if period == '24h':
        query = """
        SELECT ticker, close, LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
        FROM stock_prices_data
        WHERE date = CURRENT_DATE
        """
    elif period == '30d':
        query = """
        SELECT ticker, close, LAG(close, 30) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
        FROM stock_prices_data
        WHERE date = CURRENT_DATE
        """
    elif period == '1y':
        query = """
        SELECT ticker, close, LAG(close, 365) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
        FROM stock_prices_data
        WHERE date = CURRENT_DATE
        """
    else:
        raise ValueError("Invalid period")
    
    df = pd.read_sql(query, engine)
    df['percentage_change'] = ((df['close'] - df['prev_close']) / df['prev_close']) * 100
    return df

def get_top_gainers_losers():
    query = '''
        SELECT ticker, (close - prev_close) AS price_change
        FROM (
            SELECT ticker, close,
                   (SELECT close 
                    FROM stock_prices_data sp2
                    WHERE sp2.ticker = sp1.ticker
                      AND sp2.date < sp1.date
                    ORDER BY date DESC
                    LIMIT 1) AS prev_close
            FROM stock_prices_data sp1
            WHERE date = CURRENT_DATE
        ) AS daily_change
        ORDER BY price_change DESC
    '''
    df = pd.read_sql(query, engine)
    top_gainers = df.head(10)  # Assuming top 10 gainers
    top_losers = df.tail(10)   # Assuming bottom 10 losers
    return top_gainers, top_losers

def generate_reports():
    daily_closing_prices = get_daily_closing_prices()
    price_change_24h = get_price_change_percentage('24h')
    price_change_30d = get_price_change_percentage('30d')
    price_change_1y = get_price_change_percentage('1y')
    top_gainers, top_losers = get_top_gainers_losers()
    
    # Debugging: Check the types of the variables
    print("Type of daily_closing_prices:", type(daily_closing_prices))
    print("Type of price_change_24h:", type(price_change_24h))
    print("Type of price_change_30d:", type(price_change_30d))
    print("Type of price_change_1y:", type(price_change_1y))
    print("Type of top_gainers:", type(top_gainers))
    print("Type of top_losers:", type(top_losers))
    
    # Save to CSV if they are DataFrames
    if isinstance(daily_closing_prices, pd.DataFrame):
        daily_closing_prices.to_csv('daily_closing_prices.csv', index=False)
    else:
        print("Error: daily_closing_prices is not a DataFrame")
        
    if isinstance(price_change_24h, pd.DataFrame):
        price_change_24h.to_csv('price_change_24h.csv', index=False)
    else:
        print("Error: price_change_24h is not a DataFrame")
        
    if isinstance(price_change_30d, pd.DataFrame):
        price_change_30d.to_csv('price_change_30d.csv', index=False)
    else:
        print("Error: price_change_30d is not a DataFrame")
        
    if isinstance(price_change_1y, pd.DataFrame):
        price_change_1y.to_csv('price_change_1y.csv', index=False)
    else:
        print("Error: price_change_1y is not a DataFrame")
        
    if isinstance(top_gainers, pd.DataFrame):
        top_gainers.to_csv('top_gainers.csv', index=False)
    else:
        print("Error: top_gainers is not a DataFrame")
        
    if isinstance(top_losers, pd.DataFrame):
        top_losers.to_csv('top_losers.csv', index=False)
    else:
        print("Error: top_losers is not a DataFrame")
