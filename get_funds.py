import logging
from pathlib import Path

import requests
from pydantic import AliasPath, BaseModel, Field, field_validator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://kernelwealth.co.nz/_next/data/ymRZnwtwIAb2HNKx26G78/en/"


class FundHolding(BaseModel):
    _key: str
    company: str
    countryName: str | None
    countryCode: str | None
    proportion: float = Field(validation_alias="percentage")

    @field_validator("proportion", mode="before")
    @classmethod
    def parse_percentage(cls, v: str) -> float:
        if isinstance(v, str) and v.endswith("%"):
            return round(float(v.strip("%")) / 100, 4)
        return 0


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
