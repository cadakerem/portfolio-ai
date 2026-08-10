import yfinance as yf

def is_fund_code(ticker: str) -> bool:
    return len(ticker) == 3 and ticker.isalnum()

def is_stock_code(ticker: str) -> bool:
    return not is_fund_code(ticker)

def fetch_tefas_funds():
    import pytefas
    from datetime import datetime, timedelta
    crawler = pytefas.Crawler()
    today = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    try:
        return crawler.fetch(start=start_date, end=today)
    except:
        return None

def get_current_price(ticker, df_tefas):
    current_price = None
    
    # Check if TEFAS Fund (3 letters)
    if is_fund_code(ticker):
        if df_tefas is not None and not df_tefas.empty:
            fund_data = df_tefas[df_tefas['fund_code'] == ticker]
            if not fund_data.empty:
                fund_data = fund_data.sort_values('date')
                current_price = float(fund_data['price'].iloc[-1])
                
    # If not found in TEFAS or is a stock (yfinance)
    if current_price is None:
        stock = yf.Ticker(ticker)
        current_price = float(stock.fast_info.last_price)
        
    return current_price
