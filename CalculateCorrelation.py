import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main() -> None:
    prices_df = pd.read_csv("data/price_changes.csv", index_col="date")
    correlation = prices_df.corr()
    plt.figure(figsize=(20, 10))
    heatmap = sns.heatmap(correlation, vmin=-1, vmax=1, annot=True, cmap="BrBG")
    heatmap.set_title(
        "Correlation Between Kernel Wealth Funds", fontdict={"fontsize": 18}, pad=12
    )
    plt.savefig("media/correlation.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
