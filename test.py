import yfinance as yf

test = yf.download("0371.HK", period="2Y", auto_adjust=True)
print(test.head())
