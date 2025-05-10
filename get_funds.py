import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from pydantic import AliasPath, BaseModel, Field, field_validator

from tickers import TickerDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://kernelwealth.co.nz/_next/data/ymRZnwtwIAb2HNKx26G78/en/"
ticker_detector = TickerDetector(os.environ["OPENAI_API_KEY"])


def get_ticker(name: str, country: str) -> str:
    ticker_db = json.load(Path("tickers/tickers.json").open())  # NOQA
    ticker_dict = {entry["name"]: entry["ticker"] for entry in ticker_db}
    if name in ticker_dict:
        return ticker_dict[name]

    ticker = ticker_detector.detect(name, country)
    ticker_db.append({"name": name, "ticker": ticker})
    with Path("tickers/tickers.json").open("w") as f:
        f.write(json.dumps(ticker_db, indent=2))

    return ticker


class FundHolding(BaseModel):
    _key: str
    name: str = Field(validation_alias="company")
    ticker: str = ""
    countryName: str | None
    countryCode: str | None
    proportion: float = Field(validation_alias="percentage")

    @field_validator("proportion", mode="before")
    @classmethod
    def parse_percentage(cls, v: str) -> float:
        if isinstance(v, str) and v.endswith("%"):
            return round(float(v.strip("%")) / 100, 4)
        return 0

    def model_post_init(self, __context: Any) -> None:
        if (
            self.ticker == ""
            and self.countryName is not None
            and self.proportion >= 0.0001
        ):
            self.ticker = get_ticker(self.name, self.countryName)


def get_holdings(slug: str) -> list[FundHolding]:
    fund_url = BASE_URL + f"funds/{slug}.json"
    fund_holding_info = requests.get(fund_url, timeout=30).json()["pageProps"]["fund"][
        "fundHoldings"
    ]
    return [FundHolding.model_validate(f) for f in fund_holding_info]


class Fund(BaseModel):
    _id: str
    title: str
    slug: str = Field(validation_alias=AliasPath("slug", "current"))
    summary: str
    holdings: list[FundHolding] = Field(validation_alias=AliasPath("slug", "current"))

    @field_validator("holdings", mode="before")
    @classmethod
    def parse_holdings(cls, v: str) -> list[FundHolding]:
        return get_holdings(v)


def save_fund(fund: Fund) -> None:
    logger.info(f"Saving fund information to funds/{fund.slug}.json")
    with Path(f"funds/{fund.slug}.json").open("w") as f:
        f.write(fund.model_dump_json(indent=2))


def get_all_fund_information() -> None:
    fund_request = requests.get(BASE_URL + "funds.json", timeout=30).json()

    fund_categories = fund_request["pageProps"]["pageData"]["fundCategories"]
    fund_list = [fund for cat in fund_categories for fund in cat["funds"]]
    for fund in fund_list:
        save_fund(Fund.model_validate(fund))


def main() -> None:
    get_all_fund_information()


if __name__ == "__main__":
    main()
