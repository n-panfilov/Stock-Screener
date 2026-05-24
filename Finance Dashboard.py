#region setup
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime
from random import choice
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
current_year = datetime.now().year
pd.set_option('display.float_format', '{:,.0f}'.format)
Tickers = {}
statement_map = {
    "IS": "financials",
    "BS": "balance_sheet",
    "CFS": "cashflow"
}
PROF_RATIOS = ('Gross Margin(GM)',
               'Operating Margin(OM)',
               'Net Margin(NM)',
               'ROE','ROA'
               )
LEV_RATIOS = ('Debt/Equity(DE)',
              'Interest Coverage(IC)'
              )
VAL_RATIOS = ('P/E','P/B', 'EV/EBITDA','Dividend Yield(DY)')
EFF_RATIOS = ('Asset Turnover(AT)','Inventory Turnover(IT)')
RATIOS = (PROF_RATIOS,LEV_RATIOS,VAL_RATIOS,EFF_RATIOS)
#endregion

#region getting the stocks to look at
stock = None
while stock != '':
    stock = input("Stock symbol (Hit enter to stop entering): ")
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
    infoType = input("Please enter valid option:  ")
#endregion

#region getting the year range
temp = getattr(choice(list(Tickers.values())),choice(list(statement_map.values())))
available_years = temp.columns.year.unique().tolist()
year_range = False
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

#region building the dataFrame/finding the desired ratios
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
    exit()
else:
    ratio = None
    want_ratios = []
    print("\n Ratios:")
    for i in RATIOS:
        for j in i:
            print(j)
    print("\n")
    all_ratios = [ratio for sublist in RATIOS for ratio in sublist]
    while ratio != '':
        ratio = input("Enter ratio(cont to enter, enter to quit): ").strip().upper()
        if ratio in all_ratios:
            want_ratios.append(ratio)
        else:
            ratio = input("Invalid or Unavailable ratio, please try again: ").strip().upper()


#endregion

#region ratios output
for ratio in want_ratios:
    if ratio == 'GM':
        

#endregion
