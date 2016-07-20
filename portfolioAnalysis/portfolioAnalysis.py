import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

def compute_daily_returns(df):
    # Compute + return daily return values
    daily_rets = df.copy()
    daily_rets[1:] = (df[1:] / df[:-1].values) - 1

    return daily_rets[1:]

def compute_portfolio_stats(prices, allocs = [0.1,0.2,0.3,0.4], rfr = 0.0, sf = 252.0):
    normed_prices = prices / prices.ix[0]  # normalized prices
    alloced = normed_prices * allocs  # allocating weights accordingly
    port_vals = alloced.sum(axis=1)  # porfolio value = sum of all allocations
    daily_returns = compute_daily_returns(port_vals)
    
    cr = (port_vals[-1] / port_vals[0]) - 1  # cumulative returns
    adr = daily_returns.mean()  # avg. daily returns
    sddr = daily_returns.std()  # volatility (std dev of daily returns)
    sr = (daily_returns - rfr).mean() / (np.sqrt(sf) * (daily_returns).std()) # sharpe ratio

    return cr, adr, sddr, sr

def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs = [0.1,0.2,0.3,0.4], \
    sv = 1000000, rfr = 0.0, sf = 252.0, \
    gen_plot = True):

    # Read in adjusted closing prices for given symbols + date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    prices_SPY = prices_SPY / prices_SPY[0]
    normed_prices = prices / prices.ix[0]
    alloced = normed_prices * allocs  # allocating weights accordingly
    print "Allocation to each stock in portfolio over each day is:"
    print (alloced)

    init_port_distrib = sv * alloced
    port_vals = init_port_distrib.sum(axis=1) 

    # Get portfolio statistics 
    cr, adr, sddr, sr = compute_portfolio_stats(prices, allocs, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_vals/sv, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, ylabel="Normalized Price")
        plt.show()
        pass

    # Compute end value
    ev = sv * (cr + 1)

    return cr, adr, sddr, sr, ev

def test_code():
    # Define input parameters
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2011,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
