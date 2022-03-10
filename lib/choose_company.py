from lib.api_client import rest_api
from datetime import datetime
from functools import reduce
from pandas import isna, DataFrame
from random import choices

available_companies = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOG', 'GOOGL', 'NVDA', 'FB', 'AVGO', 'COST', 'CSCO', 'PEP', 'CMCSA', 'ADBE', 'INTC', 'AMD', 'QCOM', 'TXN', 'NFLX', 'TMUS', 'AMGN', 'HON', 'INTU', 'AMAT', 'PYPL', 'CHTR', 'SBUX', 'ISRG', 'ADP', 'MU', 'MDLZ', 'ADI', 'BKNG', 'CSX', 'GILD', 'LRCX', 'REGN', 'ATVI', 'FISV', 'VRTX', 'MRVL', 'KDP', 'MRNA', 'PANW', 'MAR', 'ABNB', 'ILMN', 'KLAC', 'AEP', 'KHC', 'NXPI', 'ASML', 'MELI', 'CTSH', 'FTNT', 'SNPS', 'ORLY', 'JD', 'ADSK', 'IDXX', 'PAYX', 'EXC', 'WDAY', 'WBA', 'CDNS', 'DXCM', 'MNST', 'MCHP', 'CTAS', 'XEL', 'LULU', 'EA', 'ODFL', 'AZN', 'TEAM', 'EBAY', 'BIDU', 'DLTR', 'ALGN', 'DDOG', 'CRWD', 'FAST', 'ROST', 'VRSK', 'BIIB', 'PCAR', 'ZS', 'ZM', 'ANSS', 'CPRT', 'SIRI', 'SGEN', 'MTCH', 'NTES', 'OKTA', 'VRSN', 'SWKS', 'SPLK', 'DOCU', 'CEG', 'PDD']
#excluded: ['LCID']
#best: LULU, FTNT, KHC
def get_best_company():
    companies_details = DataFrame(map(lambda ticker: get_one_company_details(ticker), available_companies))
    key = 'avg_pay'
    avg_age_max = companies_details['avg_age'].max()
    avg_age_min = companies_details['avg_age'].min()
    avg_age_diff = avg_age_max - avg_age_min   
    
    avg_pay_max = companies_details['avg_pay'].max()
    avg_pay_min = companies_details['avg_pay'].min()
    avg_pay_diff = avg_pay_max - avg_pay_min

    amount_of_people_max = companies_details['amount_of_people'].max()
    amount_of_people_min = companies_details['amount_of_people'].min()
    amount_of_people_diff = amount_of_people_max - amount_of_people_min

    companies_details['wage'] = 10
    companies_details.loc[companies_details['avg_age'] < avg_age_max - (avg_age_diff / 2), 'wage'] += 10
    companies_details.loc[companies_details['avg_pay'] > avg_pay_min - (avg_pay_diff / 2), 'wage'] += 10
    companies_details.loc[companies_details['amount_of_people'] < avg_pay_min + (amount_of_people_diff / 2), 'wage'] += 10

    tickers = companies_details['ticker'].tolist()
    wages = tuple(companies_details['wage'].tolist())

    best = choices(tickers, weights=wages)
    # result = reduce(lambda best, item: best if isna(item[key]) or best[key] <= item[key] else item, companies_details)
    return best


def remove_prefixes_from_price(df,column):
    if df[column].dropna().empty:
        return df[column]
    return (df[column].replace(r'[KkMm]+$', '', regex=True).astype(float) * \
        df[column].str.extract(r'[\d\.]+([KkMm]+)', expand=False).fillna(1)
        .replace(['K','k','M','m'], [10**3, 10**3, 10**6, 10**6]).astype(int))

def get_one_company_details(ticker):
    raw_key_executives = rest_api.get_key_executives(ticker)
    if raw_key_executives.empty:
        return {
            'ticker': ticker,
            'avg_age': None,
            'amount_of_people': None,
            'avg_pay': None
        }
    raw_key_executives.Pay = remove_prefixes_from_price(raw_key_executives,'Pay')

    return {
        'ticker': ticker,
        'avg_age': (datetime.now().year - raw_key_executives['Year Born']).mean(), 
        'amount_of_people': len(raw_key_executives),
        'avg_pay': raw_key_executives['Pay'].mean()
    }