import argparse
import Stocks
import dateutil.relativedelta
from datetime import date
import matplotlib.pyplot as plt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", metavar='', type=str, default='params.yaml')

    args, _ = parser.parse_known_args()

    # Declare stocks class
    stocks = Stocks.stocks(args)

    # Read params from .yaml file into Stocks class
    stocks.read_params()

    # # Calculate portfolio returns 
    # portfolio_returns = stocks.get_portfolio_returns("max", "1d")
    # plt.plot(portfolio_returns*100)
    # plt.title("Portfolio Return")
    # plt.xlabel("Date")
    # plt.ylabel("Return (%)")
    # plt.show()

    # # Calculate timeseries value of portfolio
    # stocks.get_portfolio_value_timeseries("max", "1d")
    # portfolio_value = stocks.get_portfolio_value_timeseries("max", "1d")
    # plt.plot(portfolio_value)
    # plt.title("Portfolio Book Value")
    # plt.xlabel("Date")
    # plt.ylabel("Book Value ($)")
    # plt.show()

    # Calculate timeseries values of stocks in portfolio
    portfolio_returns = stocks.get_portfolio_stock_values_timeseries("max", "1d")
    
    plt.title("Portfolio Stock Values")
    plt.xlabel("Time (days)")
    plt.ylabel("Book Value ($)")
    label_array = []
    print(portfolio_returns)
    for ticker, values in portfolio_returns.iteritems():
        print(values)
        plt.plot(values, label=ticker)
    plt.legend()
    plt.show()
    
# print("\n\n\n")
# print("Portfolio Calculator for ASX: ")
# N = int(input("Input number of assets in portfolio: "))
# assets = []
# weights = []
# tickers = ""

# for i in range(0,N):
#     asset_in = input("Input asset code: ")
#     assets.append(asset_in+".AX")
#     weights.append(float(input("Input weight(decimal fraction): ")))
#     tickers += asset_in+".AX "

# Mperiod =  float(input("Input investment period (days max 40): "))

# a_day = dateutil.relativedelta.relativedelta(days=int(Mperiod))

# endTime = date.today()
# startTime = endTime - a_day

# data = yf.download(tickers, start=startTime, end=endTime, interval="1h")

# std_assets = []


# for i in range(0,N):
#     std_assets.append(np.std(data['Close',assets[i]]))


# asset_returns = []   #   This is a N by m dimensional array
# returns = []         #   where N is number of assets and m is number of data points per asset
# return_portfolio = [0] * len(data['Close',assets[i]])
# for i in range(0,N):
#     for j in range(0,len(data['Close',assets[i]])):
#         returns.append(100*(data['Close',assets[i]].iloc[j] - data['Close',assets[i]].iloc[0]) / data['Close',assets[i]].iloc[0])   #   Return as a percentage
#     #   Calculate portfolio return
#     asset_returns.append(returns)
#     temp_ret = [k*weights[i] for k in asset_returns[i]]
#     return_portfolio = list(map(add, return_portfolio, temp_ret))
#     returns = []



# #   Calculate variance-covariance array
# cov_array = np.cov(asset_returns)

# #   Calculate portfolio standard deviation
# std_portfolio = 0
# for i in range(0,N):
#     for j in range(0,N):
#         std_portfolio += weights[i]*cov_array[i][j]*weights[j]
# std_portfolio = std_portfolio**0.5

# print("\n\n\n")
# for i in range(0,N):
#     print("%s standard deviation: %.4f\n" %(assets[i], std_assets[i]))

# print("Portfolio Standard Deviation: %.4f" %std_portfolio)

# print("\n\n\n")

# #   Display data graphically
# x1 = np.linspace(0, Mperiod, len(data['Close',assets[0]]))
# x2 = np.linspace(0, Mperiod, len(return_portfolio))

# fig, axs = plt.subplots(N+1)
# fig.tight_layout()

# for i in range(0,N):
#     axs[i].set_title(assets[i])
#     axs[i].plot(x1, data['Close',assets[i]], [np.random.rand(), np.random.rand(), np.random.rand()])
#     axs[i].set(xlabel="", ylabel="Share price ($)")

# axs[N].set_title("Portfolio Return")
# axs[N].plot(x2, return_portfolio, [np.random.rand(), np.random.rand(), np.random.rand()])
# axs[N].set(xlabel="Time (days)", ylabel="Return (%)")

# plt.plot(x2, return_portfolio, [np.random.rand(), np.random.rand(), np.random.rand()])
# plt.title("Portfolio Return")
# plt.xlabel("Time (days)")
# plt.ylabel("Return (%)")

# plt.show()