import json
import os
from pathlib import Path

import requests
from pydantic import BaseModel, Field
from pydantic_core import to_jsonable_python


class Stock(BaseModel):
    name: str
    ticker: str = Field(validation_alias="symbol")


urls = [
    f"https://chelly.kernelwealth.co.nz/api/Direct/browse-stocks?page={i}&pageSize=200"
    for i in range(1, 6)
]


shares_response = [
    requests.get(
        url, headers={"Authorization": os.environ["KERNEL_AUTH"]}, timeout=30
    ).json()["data"]
    for url in urls
]

all_stocks = [
    Stock.model_validate(stock)
    for response in shares_response
    for stock in response
]

with Path("../tickers/tickers.json").open("w") as f:
    f.write(json.dumps(to_jsonable_python(all_stocks)))
