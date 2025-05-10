import json
from pathlib import Path

import requests
from pydantic import BaseModel, Field
from pydantic_core import to_jsonable_python


class Stock(BaseModel):
    name: str
    ticker: str = Field(validation_alias="symbol")


kernel_shares_url = (
    "https://kernelwealth.co.nz/_next/data/ymRZnwtwIAb2HNKx26G78/en/shares-etfs.json"
)

shares_response = requests.get(kernel_shares_url, timeout=30).json()["pageProps"][
    "data"
]["highlightedStocks"]

all_stocks = [
    Stock.model_validate(stock)
    for section in shares_response
    for stock in section["stocks"]
]

with Path("tickers/tickers.json").open("w") as f:
    f.write(json.dumps(to_jsonable_python(all_stocks)))
