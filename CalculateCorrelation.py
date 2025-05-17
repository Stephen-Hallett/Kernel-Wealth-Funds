import json
from pathlib import Path
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
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
    coverage = float(np.sum(proportions))
    fund_prices = pd.DataFrame(data.to_numpy() @ proportions, index=data.index)
    price_changes = fund_prices.pct_change().reset_index()
    return price_changes.rename(columns={0: fund["title"]}).set_index("Date"), coverage


def main() -> None:
    yf.set_tz_cache_location(".cache")
    all_prices = []
    all_coverage = []
    for fund_path in Path("funds").glob("*.json"):
        with fund_path.open() as f:
            fund = json.load(f)
        prices, coverage = get_fund_prices(fund)
        if coverage is not None:
            all_prices.append(prices)
            all_coverage.append(coverage)
        sleep(5)
    prices_df = all_prices[0].join(all_prices[1:], how="outer", sort=True)
    coverage_df = pd.DataFrame(
        dict(zip(prices_df.columns, all_coverage, strict=False)), index=[""]
    )
    correlation = prices_df.corr()
    plt.figure(figsize=(20, 10))
    heatmap = sns.heatmap(correlation, vmin=-1, vmax=1, annot=True, cmap="BrBG")
    heatmap.set_title(
        "Correlation Between Kernel Wealth Funds", fontdict={"fontsize": 18}, pad=12
    )
    plt.savefig("media/correlation.png", dpi=300, bbox_inches="tight")

    plt.figure(figsize=(18, 2))
    coverage_heatmap = sns.heatmap(
        coverage_df, vmin=0, vmax=1, annot=True, cmap="Greens"
    )
    coverage_heatmap.set_title(
        "Proportion of Fund Where Price Data Was Retrievable",
        fontdict={"fontsize": 18},
        pad=16,
    )
    plt.savefig("media/coverage.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
