import json
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


def get_fund_prices(fund: dict) -> tuple[pd.DataFrame | None, float | None]:
    fund_makeup = {
        holding["ticker"]: holding["proportion"]
        for holding in fund["holdings"]
        if len(holding["ticker"])
    }
    if not len(fund_makeup.keys()):
        return None, None

    data = yf.download(sorted(fund_makeup.keys()), period="2y", auto_adjust=True)[
        "Close"
    ]
    data = data.ffill().dropna(axis=1)

    proportions = np.array([fund_makeup[ticker] for ticker in data.columns]).T
    coverage = np.sum(proportions)
    fund_prices = pd.DataFrame(data.to_numpy() @ proportions, index=data.index)
    return fund_prices, coverage


def main() -> None:
    yf.set_tz_cache_location(".cache")
    for fund_path in Path("funds").glob("*.json"):
        with fund_path.open() as f:
            fund = json.load(f)
        prices, coverage = get_fund_prices(fund)
        if coverage is not None:
            print(f"{fund['title']}: {coverage * 100}%")


if __name__ == "__main__":
    main()
