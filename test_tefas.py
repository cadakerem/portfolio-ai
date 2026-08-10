import pytefas, datetime
crawler = pytefas.Crawler()
today = datetime.datetime.now().strftime('%Y-%m-%d')
start = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
print('fetching...')
df = crawler.fetch(start=start, end=today)
print(df.head())