import matplotlib.pyplot as plt

def plot_moving(data,short_window=2,long_window=4):
    df = data.copy()

    df["short_ma"] = df["close"].rolling(window=short_window).mean()
    df["long_ma"] = df["close"].rolling(window = long_window).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["close"], label="Close Price")
    plt.plot(df.index, df["short_ma"], label=f"Short MA ({short_window})")
    plt.plot(df.index, df["long_ma"], label=f"Long MA ({long_window})")

    plt.title("Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)

    plt.show()