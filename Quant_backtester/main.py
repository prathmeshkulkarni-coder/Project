import pandas as pd
from statergy.moving_average import strategy
from engine.backtester import backtest
from visualization.ma_plot import plot_moving

data = pd.read_csv(r"C:\Users\Lenovo\Desktop\Quant\Project\Quant_backtester\data\prices.csv",)

data["date"] = pd.to_datetime(data["date"])

data = data.sort_values("date")
data.set_index("date",inplace=True)

signals = strategy(data)

results = backtest(data,signals)
# 1. Cumulative return
results["cumulative_return"] = (1 + results["strategy_return"]).cumprod()

# 2. Total return
total_return = results["cumulative_return"].iloc[-1] - 1
print("Total Return:", total_return)

# 3. Volatility (risk)
volatility = results["strategy_return"].std()
print("Volatility:", volatility)

# 4. Sharpe Ratio
mean_return = results["strategy_return"].mean()
sharpe_ratio = mean_return / volatility
print("Sharpe Ratio:", sharpe_ratio)

# 5. Drawdown
results["cum_max"] = results["cumulative_return"].cummax()
results["drawdown"] = (results["cumulative_return"] - results["cum_max"]) / results["cum_max"]

max_drawdown = results["drawdown"].min()
print("Max Drawdown:", max_drawdown)
print(results[["close","signal","position","price_return","strategy_return"]])

plot_moving(data)
