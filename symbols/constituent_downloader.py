import json
import logging
import requests
from pandas import DataFrame

sources = {
	'sp500': 'https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?tab=all&fileType=json',
	'russell1000': 'https://www.ishares.com/us/products/239707/ishares-russell-1000-etf/1467271812596.ajax?tab=all&fileType=json',
	'russell3000': 'https://www.ishares.com/us/products/239714/ishares-russell-3000-etf/1467271812596.ajax?tab=all&fileType=json'
}

columns = [
	'Ticker',
	'Name',
	'Sector',
	'Asset Class',
	'Market Value',
	'Weight (%)',
	'Notional Value',
	'Shares',
	'CUSIP',
	'ISIN',
	'SEDOL',
	'Share Price',
	'Country of Incorporation',
	'Exchange',
	'Base Currency',
	'FX Rate',
	#'Quote Currency',
	'Accrual Date'
]

for source, url in sources.items():
	print(f'Downloading {source} ...')
	response = requests.get(url)
	response.raise_for_status()

	response.encoding = 'utf-8-sig'
	data = response.json()['aaData']

	for row in data:
		for i in range(len(row)):
			if type(row[i]) is dict:
				row[i] = row[i]['raw']

	df = DataFrame.from_records(data, columns=columns)
	df.to_csv(source + '_constituents.csv', index=False)
