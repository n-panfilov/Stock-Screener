#region setup
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime
from random import choice
import openpyxl
import os
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
current_year = datetime.now().year
pd.set_option('display.float_format', '{:,.2f}'.format)
Tickers = {}
statement_map = {
    "IS": "financials",
    "BS": "balance_sheet",
    "CFS": "cashflow"
}
PROF_RATIOS = ('GM', 'OM','NM','ROE','ROA')
LEV_RATIOS = ('DE','IC')
VAL_RATIOS = ('PE','PB', 'EVEB','DY')
EFF_RATIOS = ('AT','IT')
RATIOS = (PROF_RATIOS,LEV_RATIOS,VAL_RATIOS,EFF_RATIOS)

ratio_display = {
    'GM': 'Gross Margin',
    'OM': 'Operating Margin',
    'NM': 'Net Margin',
    'ROE': 'Return on Equity',
    'ROA': 'Return on Assets',
    'DE': 'Debt/Equity',
    'IC': 'Interest Coverage',
    'PE': 'P/E',
    'PB': 'P/B',
    'EVEB': 'EV/EBITDA',
    'DY': 'Dividend Yield',
    'AT': 'Asset Turnover',
    'IT': 'Inventory Turnover'
}
#endregion

#region Helper Methods
def get_line_item(statement, *possible_names):
    for name in possible_names:
        if name in statement.index:
            return statement.loc[name]
    return None
#endregion

#region getting the stocks to look at
stock = None
while stock != '':
    stock = input("Stock symbol (Hit enter to stop entering): ").strip().upper()
    if stock =='':
        break
    #checking if actual ticker
    test = yf.Ticker(stock)
    hist = test.history(period = '1d')
    if hist.empty:
        print('Not a valid Ticker')
        continue
    Tickers[stock] = test
#endregion

#region getting the info user wants to see
infoType = input("Would you like the BS, IS, CFS, or RATIOS?: ").strip().upper()
while infoType not in ['BS','IS','CFS','RATIOS']:
    infoType = input("Please enter valid option:  ").strip().upper()
#endregion

#region getting the year range
temp = getattr(choice(list(Tickers.values())),choice(list(statement_map.values())))
available_years = temp.columns.year.unique().tolist()
year_range = False

if infoType == "RATIOS":
    while True:
        start_year = input("Enter year: ").strip()
        try:
            start_year = int(start_year)
            if start_year in available_years:
                break
            else:
                print(f"Available years: {available_years}")
        except ValueError:
            start_year = input("Invalid or unavailable year, please try again:  ").strip()
else:

    while True:
        start_year = input("Enter start year or only year(earliest): ").strip()
        try:
            start_year = int(start_year)
            if start_year in available_years:
                break
            else:
                print(f"Available years: {available_years}")
        except ValueError:
            start_year = input("Invalid or unavailable year, please try again:  ").strip()
    while True:
        end_year = input("Enter end year or hit enter to leave a single year(closest to present): ").strip()
        if end_year =='':
            year_range = False
            break
        try:
            end_year = int(end_year)
            if end_year in available_years:
                year_range = True
                break
            else:
                print(f"Available years: {available_years}")
        except ValueError:
            end_year = input("Invalid or unavailable year, please try again:  ").strip()

#endregion

#region Main body of result creation
#region building the dataFrame/finding the desired ratios
tickers_string = "_".join(Tickers.keys()).replace('.','-')
date_str = datetime.now().strftime("%Y-%m-%d")
downloads = os.path.join(os.path.expanduser("~"),"Downloads")

compare = {}
if infoType != 'RATIOS':
    statement_name = statement_map[infoType]
    for symbol, data in Tickers.items():
        statement = getattr(data, statement_name)
        if year_range:
            compare[symbol] = statement.loc[:,(statement.columns.year >= start_year) & (statement.columns.year <= end_year)]
        else:
            compare[symbol] = statement.loc[:, statement.columns.year == start_year]

    pd_full = pd.concat(compare, axis =1, sort = False)
    print(pd_full)
    pd_full.to_excel(os.path.join(downloads, f"Stock Screener Results_{tickers_string}_{infoType}_{date_str}.xlsx"))

    exit()
else:
    print("\nRatios:")
    for abbrev, full_name in ratio_display.items():
        print(f"{abbrev}: {full_name}")
    print("\n")
    ratio = None
    want_ratios = []
    all_ratios = [ratio for sublist in RATIOS for ratio in sublist]
    while True:
        ratio = input("Enter ratio(cont to enter, enter to quit): ").strip().upper()
        if ratio in all_ratios:
            want_ratios.append(ratio)
        elif ratio == 'ALL':
            want_ratios = all_ratios
            break
        else:
            print("Invalid or Unavailable ratio, please try again: ")

#endregion

#region ratios output

for ticker,item in Tickers.items():
    income = item.financials
    balance = item.balance_sheet
    if year_range:
        income = income.loc[:, (income.columns.year >= start_year) & (income.columns.year <= end_year)]
        balance = balance.loc[:, (balance.columns.year >= start_year) & (balance.columns.year <= end_year)]
    else:
        income = income.loc[:, income.columns.year == start_year]
        balance = balance.loc[:, balance.columns.year == start_year]
    sector = item.info.get("sector")
    is_financial = sector == "Financial Services"
    ratio_values = {}
    for ratio in want_ratios:
        if ratio == 'GM':
            if is_financial:
                ratio_values[ratio_display[ratio]] = "N/A"
            else:
                gross_profit = get_line_item(income,"Gross Profit","Gross Revenue","Gross Income","Total Gross Profit","Total Gross Income","Total Gross Revenue")
                total_revenue = get_line_item(income, "Total Revenue" ,"Total Income" , "Total Profit")
                if gross_profit is not None and total_revenue is not None:
                    ratio_values[ratio_display[ratio]] = f"{(gross_profit/total_revenue).iloc[0] * 100:.2f}%"
                else:
                    ratio_values[ratio_display[ratio]] = None
        elif ratio == 'OM':
            if is_financial:
                ratio_values[ratio_display[ratio]] = "N/A"
            else:
                operating_income = get_line_item(income, "Operating Income","Operating Revenue")
                total_revenue = get_line_item(income, "Total Revenue" ,"Total Income" , "Total Profit")
                if operating_income is not None and total_revenue is not None:
                    ratio_values[ratio_display[ratio]] = f"{(operating_income/total_revenue).iloc[0] *100:.2f}%"
                else:
                    ratio_values[ratio_display[ratio]] = None
        elif ratio == "NM":
            net_income = get_line_item(income,"Net Income","Net Profit","Net Earnings","Net Revenue")
            total_revenue = get_line_item(income, "Total Revenue", "Total Income", "Total Profit")
            if net_income is not None and total_revenue is not None:
                ratio_values[ratio_display[ratio]] = f"{(net_income/total_revenue).iloc[0] * 100:.2f}%"
            else:
                ratio_values[ratio_display[ratio]] = None
        elif ratio == "ROE":
            net_income = get_line_item(income,"Net Income","Net Profit","Net Earnings","Net Revenue")
            total_sh_equity = get_line_item(balance,"Total Shareholder Equity","Total Shareholders Equity","Total Shareholder's Equity","Stockholders Equity")
            if net_income is not None and total_sh_equity is not None:
                ratio_values[ratio_display[ratio]] = f"{(net_income/total_sh_equity).iloc[0] *100:.2f}%"
            else:
                ratio_values[ratio_display[ratio]] = None
        elif ratio == "ROA":
            net_income = get_line_item(income,"Net Income","Net Profit","Net Earnings","Net Revenue")
            total_assets = get_line_item(balance,"Total Assets")
            if net_income is not None and total_assets is not None:
                ratio_values[ratio_display[ratio]] = f"{(net_income/total_assets).iloc[0] * 100:.2f}%"
            else:
                ratio_values[ratio_display[ratio]] = None
        elif ratio == "DE":
            total_debt = get_line_item(balance,"Total Debt", )
            total_sh_equity = get_line_item(balance,"Total Shareholder Equity","Total Shareholders Equity","Total Shareholder's Equity", "Stockholders Equity")
            if total_debt is not None and total_sh_equity is not None:
                ratio_values[ratio_display[ratio]] = (total_debt/total_sh_equity).iloc[0]
            else:
                ratio_values[ratio_display[ratio]] = None
        elif ratio == 'IC':
            if is_financial:
                ratio_values[ratio_display[ratio]] = "N/A"
            else:
                EBIT = get_line_item(income,"EBIT","Earnings Before Interest and Tax","Earnings Before Interest & Tax","Earnings Before Interest, Tax","Earnings Before Interest Tax")
                interest_expense = get_line_item(income, "Interest Expense")
                if EBIT is not None and interest_expense is not None:
                    ratio_values[ratio_display[ratio]] = (EBIT/interest_expense).iloc[0]
                else:
                    ratio_values[ratio_display[ratio]] = None
        elif ratio == "PE":
             ratio_values[ratio_display[ratio]]= item.info.get("trailingPE")
        elif ratio == "PB":
            ratio_values[ratio_display[ratio]] = item.info.get("priceToBook")
        elif ratio == "EVEB":
            ratio_values[ratio_display[ratio]] = item.info.get("enterpriseToEbitda")
        elif ratio == "DY":
            ratio_values[ratio_display[ratio]] = item.info.get("dividendYield")
        elif ratio == "AT":
            total_revenue = get_line_item(income, "Total Revenue" ,"Total Income" , "Total Profit")
            total_assets = get_line_item(balance,"Total Assets")
            if total_assets is not None and total_revenue is not None:
                ratio_values[ratio_display[ratio]] = (total_revenue/total_assets).iloc[0]
            else:
                ratio_values[ratio_display[ratio]] = None
        elif ratio == "IT":
            if is_financial:
                ratio_values[ratio_display[ratio]] = "N/A"
            else:
                COGS = get_line_item(income, "COGS","Cogs","Cogas","COGAS","Cost of Goods Sold","Cost of Revenue")
                inventory = get_line_item(balance,"Inventory")
                if inventory is not None and COGS is not None:
                    avr_inventory = (inventory + inventory.shift(-1)) /2
                    ratio_values[ratio_display[ratio]] = (COGS/avr_inventory).iloc[0]
                else:
                    ratio_values[ratio_display[ratio]] = None
    compare[ticker] = pd.Series(ratio_values)

pd_full = pd.concat(compare, axis=1, sort = False)
print(pd_full)

pd_full.to_excel(os.path.join(downloads,f"Stock Screener Results_{tickers_string}_{infoType}_{date_str}.xlsx"))
#endregion
#endregion