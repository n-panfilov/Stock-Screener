# Stock-Screener
A Python stock screener using Yahoo Finance

# Stock Financial Dashboard

A command-line tool for pulling and comparing financial statements 
and ratios across multiple public companies using live market data.

## What it does

- Accepts multiple stock tickers and validates them against live data
- Pulls income statements, balance sheets, or cash flow statements
- Filters by a custom year or year range
- Displays a side-by-side comparison across all entered companies
- Ratio analysis module in progress (profitability, leverage, 
  valuation, efficiency)

## Built with

- Python
- yfinance
- pandas

## How to run

Install dependencies:
pip install yfinance pandas

Then run:
python "Finance Dashboard.py"

## Status

Core financial statement comparison is complete. 
Ratio calculations are currently being added.
