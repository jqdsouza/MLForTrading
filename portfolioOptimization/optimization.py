import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy.optimize import minimize
from util import get_data, plot_data

def compute_daily_returns(df):
    # Compute + return daily return values
    daily_rets = df.copy()
    daily_rets[1:] = (df[1:] / df[:-1].values) - 1

    return daily_rets[1:]

def compute_portfolio_stats(prices, start_val, allocs = [0.1,0.2,0.3,0.4], rfr = 0.0, sf = 252.0):
    normed_prices = prices / prices.ix[0]  # normalized prices
    alloced = normed_prices * allocs  # allocating weights accordingly
    port_vals = alloced.sum(axis=1)  # porfolio value is sum of all allocations
    daily_returns = compute_daily_returns(port_vals)
    
    cr = (port_vals[-1] / port_vals[0]) - 1  # cumulative returns
    adr = daily_returns.mean()  # avg. daily returns
    sddr = daily_returns.std()  # volatility (std dev of daily returns)
    sr = (daily_returns - rfr).mean() / (np.sqrt(sf) * (daily_returns).std()) # sharpe ratio

    return cr, adr, sddr, sr, port_vals

def function(allocs, prices, start_val = 1000000, rfr = 0.0, sf = 252.0):
    cr, adr, sddr, sr, port_val = compute_portfolio_stats(prices, start_val, allocs, rfr, sf)

    return -sr

def optimize_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols + date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find allocations for optimal portfolio
    estimate = np.ones(len(syms)) * (1.0/len(syms))
    bounds = [(0,1.0) for i in range(len(syms))]
    allocs = minimize(function, estimate, args=(prices,), bounds=bounds, method='SLSQP', 
                            options={'disp':True}, 
                            constraints=({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)})).x

    cr, adr, sddr, sr, port_val = compute_portfolio_stats(prices, start_val=1.0, allocs=allocs, rfr=0.0, sf=252.0)

    # Get daily portfolio value
    normed_prices = prices / prices.ix[0]  # normalized prices
    alloced = normed_prices * allocs  # allocating weights accordingly
    port_vals = alloced.sum(axis=1)  # porfolio value is sum of all allocations
    port_val = compute_daily_returns(port_vals)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_vals, prices_SPY/prices_SPY[0]], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, ylabel="Normalized Price")
        plt.show()
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
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

