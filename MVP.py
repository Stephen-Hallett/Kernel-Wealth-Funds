import numpy as np
import pandas as pd
from scipy.optimize import minimize


def minimum_variance(ret: pd.DataFrame) -> list:
    def find_port_variance(weights: np.ndarray) -> np.ndarray:
        # this is actually std
        cov = ret.cov()
        return np.sqrt(np.dot(weights.T, np.dot(cov, weights)) * 250)

    def weight_cons(weights: np.ndarray) -> float:
        return np.sum(weights) - 1

    bounds_lim = [
        (0, 1) for x in range(len(ret.columns))
    ]  # change to (-1, 1) if you want to short
    init = [1 / len(ret.columns) for i in range(len(ret.columns))]
    constraint = {"type": "eq", "fun": weight_cons}

    optimal = minimize(
        fun=find_port_variance,
        x0=init,
        bounds=bounds_lim,
        constraints=constraint,
        method="SLSQP",
    )

    return list(optimal["x"])


def max_sharpe(ret: pd.DataFrame) -> list:
    def sharpe_func(weights: np.ndarray) -> float:
        hist_mean = ret.mean(axis=0).to_frame()
        hist_cov = ret.cov()

        port_ret = np.dot(weights.T, hist_mean.values) * 250
        port_std = np.sqrt(np.dot(weights.T, np.dot(hist_cov, weights)) * 250)
        return -1 * port_ret / port_std

    def weight_cons(weights: np.ndarray) -> float:
        return np.sum(weights) - 1

    bounds_lim = [
        (0, 1) for x in range(len(ret.columns))
    ]  # change to (-1, 1) if you want to short
    init = [1 / len(ret.columns) for i in range(len(ret.columns))]
    constraint = {"type": "eq", "fun": weight_cons}

    optimal = minimize(
        fun=sharpe_func,
        x0=init,
        bounds=bounds_lim,
        constraints=constraint,
        method="SLSQP",
    )

    return list(optimal["x"])


def main() -> None:
    prices_df = pd.read_csv("data/price_changes.csv", index_col="date")
    returns = prices_df + 1
    sharpe_weights = max_sharpe(returns)
    mvp_weights = minimum_variance(returns)
    for i, fund in enumerate(returns.columns):
        print(f"{fund}: Sharpe: {sharpe_weights[i]}, MVP: {mvp_weights[i]}")


if __name__ == "__main__":
    main()
