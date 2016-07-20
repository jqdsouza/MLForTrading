# MLForTrading

Following are a series of projects I've implemented with the goal of applying machine learning to solve classic trading problems: 

<b> portfolioAnalysis </b>: This project takes as input a description of a portfolio and computes important statistics about it.

<i>Inputs:</i>
<li> A date range to select the historical data to use (specified by a start and end date). </li> 
<li> Symbols for equities</li>
<li> Allocations to the equities at the beginning of the simulation </li>
<li> Total starting value of the portfolio </li>

<i>Statistics computed:</i>
<li>Cumulative return</li>
<li>Average period return</li>
<li>Standard deviation of daily returns</li>
<li>Sharpe ratio of the overall portfolio, given daily risk free rate and yearly sampling frequency </li>
<li>Ending value of the portfolio</li>

<b> portfolioOptimization </b>: The goal of this project was to find the optimal allocations for a given set of stocks. This is done by optimizing for Sharpe ratio.

<i> Input parameters: </i>
<li>sd: A datetime object that represents the start date</li>
<li>ed: A datetime object that represents the end date</li>
<li>syms: A list of symbols that make up the portfolio</li>
<li>gen_plot: If True, creates a plot named plot.png</li>

<i> Outputs: </i>
<li>allocs: A 1-d Numpy ndarray of allocations to the stocks</li>
<li>cr: Cumulative return</li>
<li>adr: Average daily return</li>
<li>sddr: Standard deviation of daily return</li>
<li>sr: Sharpe ratio</li>
<li>The input parameters are:</li>

<b> marketSimulator </b>: A market simulator that accepts trading orders and keeps track of a portfolio's value over time and then assesses the performance of that portfolio.



