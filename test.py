import yfinance as yf

test = yf.download("IBM", period="2Y", auto_adjust=True)
print(test.head())
