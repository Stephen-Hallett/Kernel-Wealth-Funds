import os

from tickers import TickerDetector

ticker_detector = TickerDetector(os.environ["OPENAI_API_KEY"])

print(ticker_detector.detect("National Grid PLC Ord", "Great Britain"))
