# Financial Analysis Dashboard

A Python tool for pulling and analyzing public company financial data using the Yahoo Finance API.

## Features

- Pull Income Statements, Balance Sheets, and Cash Flow Statements for multiple companies side by side
- Calculate and compare 13 key financial ratios across companies
- Automatic sector detection — flags N/A for ratios not applicable to financial sector companies
- Filter by year or year range
- Exports results to a timestamped Excel file

## Ratios Supported

**Profitability:** Gross Margin, Operating Margin, Net Margin, ROE, ROA

**Leverage:** Debt/Equity, Interest Coverage

**Valuation:** P/E, P/B, EV/EBITDA, Dividend Yield

**Efficiency:** Asset Turnover, Inventory Turnover

## Setup

```bash
pip install yfinance pandas openpyxl
```

## Usage

Run the script and follow the prompts to enter ticker symbols, select output type, and choose a year range. Results print to the terminal and export to your Downloads folder.

## Tech Stack

Python, yfinance, pandas, openpyxl