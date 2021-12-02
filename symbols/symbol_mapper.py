import pandas as pd
import pickle
import random
import requests
import time
import sys
from os import path
from typing import Any

import config

mapping_cache_filename = 'symbol_mapper_cache.pickle'

noise = [
	'adr',
	'ag',
	'co',
	'company',
	'corp',
	'corporation',
	'group',
	'grp',
	'holdings',
	'i',
	'ii',
	'inc',
	'incorporated',
	'limited',
	'llc',
	'ltd',
	'plc',
	'preferred',
	'stock',
	'trust',
	'v',
]

hardcoded_mappings = {
	'BFB': 'BF-B'
}

def main():
	if len(sys.argv) != 2:
		log('Usage: symbol_mapper.py <input.csv>')
		return

	df = read_constituents(sys.argv[1])
	cache = read_mappings_cache()

	try:
		map_instruments(df, cache)
	finally:
		save_mappings_cache(cache)

def map_instruments(df: pd.DataFrame, cache: dict[str, str]) -> None:
	count = 0
	total = len(df)
	for instrument, row in df.iterrows():
		count += 1
		
		if instrument in cache:
			print(cache[instrument])
			continue

		log(f'{instrument} {count}/{total}')
		result = try_map_instrument(instrument, row)
		cache[instrument] = result
		print(result)

def try_map_instrument(instrument: str, row: pd.Series) -> str:
		company_name = row['Name']
		company_name_clean = clean_company_name(company_name)
		instrument_clean = clean_instrument(instrument)

		for tentative in range(3):
			results: list[dict[str, str]] = []
			if tentative == 0:
				results = symbol_search(instrument_clean)
			elif tentative == 1:
				results = symbol_search(company_name_clean)
			elif tentative == 2:
				short_name = ' '.join(company_name.split(' ')[:2])
				results = symbol_search(short_name)

			log(f'Tentative {tentative + 1}')

			results = list(filter(lambda x: x['2. name'], results))
			results = list(filter(lambda x: x['3. type'] == 'Equity', results))
			results = list(filter(lambda x: x['4. region'] == 'United States', results))

			ticker_matched = False
			if len(results) > 1:
				results2 = list(filter(lambda x: x['1. symbol'] == instrument_clean, results))
				if len(results2) > 0:
					results = results2
					ticker_matched = True
			if len(results) > 1:
				results2 = list(filter(lambda x: x['1. symbol'].replace('-', '') == instrument_clean, results))
				if len(results2) > 0:
					results = results2
					ticker_matched = True
			if len(results) > 1:
				results2 = list(filter(lambda x: x['1. symbol'].startswith(instrument_clean), results))
				if len(results2) > 0:
					results = results2
			if len(results) > 1:
				results2 = list(filter(lambda x: clean_company_name(x['2. name']) == company_name_clean, results))
				if len(results2) > 0:
					results = results2

			if len(results) > 1 and not ticker_matched:
				symbols = [x['1. symbol'] for x in results]
				log(f'Ambiguous mapping: {symbols}')
			if len(results) == 0:
				log(f'No mapping found')
			else:
				symbol = results[0]['1. symbol']
				log(f'{instrument}, {company_name} mapped to {symbol}')
				return symbol

		raise Warning('Mapping not found')

def clean_company_name(name: str) -> str:
	name = name.lower()
	name = name.replace('-', '')
	name = name.replace('.', '')
	name = name.replace(',', '')
	name = name.replace('\'', '`')
	tokens = name.split(' ')
	tokens_filtered = filter(lambda x: x not in noise, tokens)
	tokens_filtered = filter(lambda x: len(x) > 0, tokens)
	name = ' '.join(tokens_filtered)
	return name

def clean_instrument(instrument: str) -> str:
	instrument_clean = instrument.strip().upper()
	instrument_clean = hardcoded_mappings.get(instrument, instrument)
	return instrument_clean

def symbol_search(keywords: str) -> list[dict[str, str]]:
	payload = {
		'function': 'SYMBOL_SEARCH',
		'keywords': keywords,
		'apikey': config.alpha_vantage_api_key
	}
	data = make_request(payload).json()
	return data['bestMatches']

def make_request(payload: Any) -> Any:
	retry = 3
	while True:
		try:
			response = requests.get('https://www.alphavantage.co/query', params=payload)
			response.raise_for_status()
			return response
		except requests.HTTPError as e:
			retry -= 1
			if retry == 0:
				raise e
			else:
				log(e)
				time.sleep(random.randint(10, 30))


def read_constituents(filename: str) -> pd.DataFrame:
	df = pd.read_csv(filename, index_col=0)
	df = filter_equities(df)
	return df

def filter_equities(df: pd.DataFrame) -> pd.DataFrame:
	return df[df['Asset Class'] == 'Equity']

def read_mappings_cache() -> dict[str, str]:
	cache: dict[str, str] = {}
	if path.isfile(mapping_cache_filename):
		with open(mapping_cache_filename, 'rb') as file:
			cache = pickle.load(file)
	return cache

def save_mappings_cache(cache: dict[str, str]) -> None:
	with open(mapping_cache_filename, 'wb') as file:
		pickle.dump(cache, file)

def log(msg: str) -> None:
	sys.stderr.write(msg)
	sys.stderr.write('\n')

if __name__=="__main__":
	main()
