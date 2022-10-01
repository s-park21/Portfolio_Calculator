import yaml
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import dateutil.relativedelta
import numpy as np
import pandas as pd
from pprint import pprint
from operator import add


class stocks:
    def __init__(self, args):
        self.params_file = args.params
        self.tickers_all = ""
        self.tickers_current = ""
        self.current_stocks = []
        self.all_stocks = []

    def read_params(self):
        """
            Read parameters from .yaml file into class
            .yaml file should be passed into args when initialising the class
            Inputs: None
            Returns: None
        """
        
        with open(self.params_file, 'r') as stream:
            self.params_dict = yaml.safe_load(stream)
        # Data is loaded into a dict.
        # params_dict['stocks'] returns array for every stock.
        # params_dict['stocks'][10]['ticker'] returns the ticker
        # for the 10th stock.

        # Put tickers into one long string
        for stock in self.params_dict['stocks']:
            # Check for duplicate tickers
            if stock['ticker'] not in self.tickers_all:
                self.tickers_all += stock['ticker'] + " "
            # Create array of currently active stocks
            if stock["sale_date"] == "":
                self.tickers_current += stock['ticker'] + " "
                self.current_stocks.append(stock)
            self.all_stocks.append(stock)
            

    def get_stock_data(self, tickers, startDate, endDate, interval="1h"):
        """
            Gets stock data for every stock in portfolio
            Inputs: 
                startDate: datetime.date() object to specify the start date of the period
                endDate: datetime.date() object to specify the end date of the period
                interval: String that can take the form "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
            Returns: raw stock data
        """
        # Data from ABC.AX can be obtained by the following:
        # print(self.raw_stock_data['Adj Close',"ABC.AX"])

        # Load data from Yahoo finance API
        return yf.download(tickers, start=startDate, end=endDate)
        


    def get_stock_data(self, tickers, period="ytd", interval="1h"):
        """
            Gets stock data for every stock in portfolio
            Inputs: 
                tickers: String of all tickers separated by spaces
                period: String that can take the form "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
                interval: String that can take the form "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
            Returns: raw stock data
        """
        # Data from ABC.AX can be obtained by the following:
        # print(self.raw_stock_data['Adj Close',"ABC.AX"])

        # Load data from Yahoo finance API
        return yf.download(tickers, period=period, interval=interval)
    
    def get_current_price(self):
        """
            Gets current prices of an string of tickers
            Inputs: none
            Returns: array of current prices
        """
        # a_day = dateutil.relativedelta.relativedelta(days=int(1))
        # today = date.today()
        # yesterday = today - a_day
        data = yf.download(self.tickers_current, period="1d")
        return data["Adj Close"]
    
    def get_portfolio_value(self) -> float:
        """
            Gets total portfolio value today
            Inputs: None
            Returns: Float as total portfolio value in $
        """
        data = self.get_current_price()

        portfolio_value=0
        for stock in self.current_stocks:
            ticker = stock["ticker"]
            qty = stock["number"]
            portfolio_value += float(data["Adj Close", ticker]) * qty

        return portfolio_value

    def get_stock_returns(self, tickers, period, interval):
        """
            Gets stock returns 
            Inputs: 
                tickers: String of all tickers separated by spaces
                period: String that can take the form "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
                interval: String that can take the form "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
            Returns: History of returns for stocks
        """
        data = self.get_stock_data(tickers, period, interval)
        price_history = data["Adj Close"]

        # Calculate fractional change in stock prices from start of period
        for stock in data:
            price_history[stock["ticker"]] = (price_history[stock["ticker"]] - price_history[stock["ticker"]].iloc[0]) / price_history[stock["ticker"]].iloc[0]
        return price_history

    def get_portfolio_returns(self, period, interval):
        """
            Gets portfolio returns not including brokerage fees
            Inputs: 
                tickers: String of all tickers separated by spaces
                period: String that can take the form "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
                interval: String that can take the form "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
            Returns: History of returns for portfolio
        """
        stock_prices = self.get_stock_data(self.tickers_current, period, interval)["Adj Close"]
        stock_prices["Date"] = stock_prices.reset_index()['Date']

        returns = []
        stock_values= []
        # # Calculate returns of individual stocks
        for stock in self.current_stocks:
            idx =  stock_prices[stock["ticker"]].index.get_loc(stock["purchase_date"], method='nearest')
            # Filter data from purchase date
            filtered_prices = stock_prices[stock["ticker"]].iloc[idx:-1]
            inital_price = stock_prices[stock["ticker"]].iloc[idx]
            stock_return = (filtered_prices - inital_price) / inital_price
            # Calculate timeseries of weights
            stock_values.append(filtered_prices * stock["number"])
            returns.append(stock_return)

        returns = pd.DataFrame(returns).transpose()
        stock_values = pd.DataFrame(stock_values).transpose()
        # Calculate total portfolio value at any given time
        total_values = stock_values.sum(axis=1)
        weights = stock_values.divide(total_values, axis=0)

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(stock_values)
        weighted_returns = returns * weights
    
        return weighted_returns.sum(axis=1)

    def get_portfolio_value_timeseries(self, period, interval):
        """
            Gets timeseries return of portfolio
            Inputs: 
                tickers: String of all tickers separated by spaces
                period: String that can take the form "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
                interval: String that can take the form "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
            Returns: History of returns for portfolio
        """
        stock_prices = self.get_stock_data(self.tickers_current, period, interval)["Adj Close"]
        stock_prices["Date"] = stock_prices.reset_index()['Date']

        returns = []
        stock_values= []
        # # Calculate returns of individual stocks
        for stock in self.current_stocks:
            idx =  stock_prices[stock["ticker"]].index.get_loc(stock["purchase_date"], method='nearest')
            # Filter data from purchase date
            filtered_prices = stock_prices[stock["ticker"]].iloc[idx:-1]
            stock_values.append(filtered_prices * stock["number"])

        stock_values = pd.DataFrame(stock_values).transpose()
        print(stock_values.sum(axis=1))
        # Calculate total portfolio value at any given time
        return stock_values.sum(axis=1)

    def get_portfolio_stock_values_timeseries(self, period, interval):
        """
            Gets timeseries values of individual stocks within porfolio
            Inputs: 
                tickers: String of all tickers separated by spaces
                period: String that can take the form "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
                interval: String that can take the form "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
            Returns: History of returns for portfolio
        """
        stock_prices = self.get_stock_data(self.tickers_current, period, interval)["Adj Close"]
        stock_prices["Date"] = stock_prices.reset_index()['Date']

        returns = []
        stock_values= []
        # # Calculate returns of individual stocks
        for stock in self.current_stocks:
            idx =  stock_prices[stock["ticker"]].index.get_loc(stock["purchase_date"], method='nearest')
            # Filter data from purchase date
            filtered_prices = stock_prices[stock["ticker"]].iloc[idx:-1]

            stock_values.append(filtered_prices * stock["number"])

        stock_values = pd.DataFrame(stock_values).transpose()
        # Calculate total portfolio value at any given time
        return stock_values.groupby(stock_values.columns, axis=1).sum()

