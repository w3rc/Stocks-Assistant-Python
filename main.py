from matplotlib import style
from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf

import pickle
import sys
import datetime as dt



# SAVING DATA IN PORTFOLIO

# portfolio = {
#     'IRCTC': 10,
#     'IRFC' : 15,
#     'RELIANCE': 3
# }

# with open('portfolio.pkl', 'wb') as f:
#     pickle.dump(portfolio, f)

# LOADING DATA FROM PORTFOLIO

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

print(portfolio)

def greetuser():
    print('Hey there')

def save_portfolio(portfolio_data):
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio_data, f)

def add_portfolio():
    ticker_symbol = input("Enter the stock symbol to buy")
    amount = input(f"Enter the quantity of {ticker_symbol}")

    if ticker_symbol in portfolio.keys():
        portfolio[ticker_symbol] += amount
    else: 
        portfolio[ticker_symbol] = amount

    save_portfolio(portfolio)


def remove_portfolio():
    ticker_symbol = input("Enter the stock symbol to sell")
    amount = input(f"Enter the quantity of {ticker_symbol}")

    if ticker_symbol in portfolio.keys():
        if portfolio[ticker_symbol] >= int(amount):
            portfolio[ticker_symbol] -= int(amount)
            save_portfolio(portfolio)
        else:
            print("You dont have enough shares")
    else: 
        print("You dont have that stock")


def show_portfolio(): 
    for ticker in portfolio.keys():
        print(f"You own {portfolio[ticker]} shares of {ticker}")


def portfolio_worth():
    sum = 0
    for ticker in portfolio.keys():
        data = web.DataReader(ticker, 'yahoo')
        price = data['Close'].iloc[-1]
        sum += price

    print(f"Your portfolio is worth {sum} INR")

def portfolio_gains():
    start_date = input("Enter the starting date (YYYY-MM-DD): ")
    sum_now = 0
    sum_then = 0

    try:
        for ticker in portfolio.keys():
            data = web.DataReader(ticker, 'yahoo')
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index == start_date]['Close'].values[0]

            sum_now += price_now
            sum_then += price_then

            absolute_profit = sum_now - sum_then
            relative_profit = ((sum_now - sum_then)/sum_then)*100

        print(f'Profit: {absolute_profit} INR')
        print(f'Profit Percentage: {relative_profit}%')

    except IndexError:
        print('No Stock was purchased/sold on this date')


def plot_chart():
    ticker = input("Enter the stock symbol")
    start_date_string = input("Enter the starting date (DD-MM-YY)")

    plt.style.use('dark_background')
    
    start = dt.datetime.strptime(start_date_string, "%d-%m-%Y")
    end = dt.datetime.now()

    data = web.DataReader(ticker, 'yahoo', start, end)

    colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='#777777', volume='in')

    mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)
    
    mpf.plot(data, type='candle', style=mpf_style)

def bye():
    print('Goodbye')
    sys.exit(0)


mappings = {
    'greetings': greetuser,
    'plot_chart': plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_gains': portfolio_gains,
    'portfolio_worth': portfolio_worth,
    # 'bye': bye
    
}

assistant = GenericAssistant('intents.json', intent_methods=mappings)

assistant.train_model()
assistant.save_model()

while True:
    message = input("")
    assistant.request(message)