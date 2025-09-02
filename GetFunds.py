from functools import reduce

import pandas as pd
import requests

from Login import get_kernel_token

headers = {"Authorization": f"Bearer {get_kernel_token()}"}
marketplace = requests.get(
    "https://chelly.kernelwealth.co.nz/api/Marketplace", headers=headers, timeout=5
).json()

funds = marketplace["funds"]

fund_prices = []
for fund in funds:
    data = pd.DataFrame(fund["fundPriceHistory"])
    data["date"] = pd.to_datetime(data["date"]).dt.date
    data = data.drop("fundId", axis=1).rename(columns={"price": fund["slug"]})
    fund_prices.append(data)


merged_funds = reduce(
    lambda left, right: left.merge(right, on="date", how="outer"), fund_prices
)
merged_funds = merged_funds.set_index("date")
merged_funds = merged_funds.ffill().pct_change().reset_index()
merged_funds.to_csv("data/price_changes.csv", index=False)
