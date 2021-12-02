import logging
import random
import requests
import time
from datetime import date
from typing import Any, Optional

import config
from models import CompanyOverview, DataPoint, TimeSeries

def get_time_series_compact(symbol: str) -> TimeSeries:
	logging.debug(f'get_time_series_compact {symbol}')
	return _request_time_series(symbol, False)

def get_time_series_full(symbol: str) -> TimeSeries:
	logging.debug(f'get_time_series_full {symbol}')
	return _request_time_series(symbol, True)

def get_company_overview(symbol: str) -> CompanyOverview:
	logging.debug(f'get_company_overview {symbol}')
	payload = {
		'function': 'OVERVIEW',
		'symbol': symbol,
		'apikey': config.alpha_vantage_api_key
	}
	data = _make_request(payload)
	if 'Symbol' not in data:
		logging.error(f'Unexpected data format {data}')
		raise Exception('get_company_overview failed')
	return _map_company_overview(data)

def _request_time_series(symbol: str, full: bool) -> TimeSeries:
	payload = {
		'function': 'TIME_SERIES_DAILY_ADJUSTED',
		'symbol': symbol,
		'outputsize': 'full' if full else 'compact',
		'apikey': config.alpha_vantage_api_key
	}
	data = _make_request(payload)
	if 'Time Series (Daily)' not in data:
		logging.error(f'Unexpected data format {data}')
		raise Exception('_request_time_series failed')
	time_series = data['Time Series (Daily)']
	logging.info(f'Downloaded {len(time_series)} datapoints for {symbol}')
	return _parse_time_series(time_series)

def _parse_time_series(time_series: Any) -> TimeSeries:
	timeseries = list(map(lambda x: _map_datapoint(*x), time_series.items()))
	timeseries.sort(key=lambda x: x.date_)
	return timeseries

def _make_request(payload: Any) -> Any:
	data = {}
	for _ in range(3):
		data = _make_http_request(payload).json()
		if 'Error Message' in data:
			logging.error(f'Error: {data}')
			raise Exception('_request_time_series failed')
		if 'Information' in data:
			logging.info(f'Rate limit hit: {data}')
			time.sleep(random.randint(10, 30))
		else:
			break
	else:
		raise Exception('_make_request failed')
	return data

def _make_http_request(payload: Any) -> requests.Response:
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
				logging.error(e)
				time.sleep(random.randint(10, 30))

def _map_datapoint(datestr: str, data: Any) -> DataPoint:
	return DataPoint(
		float(data['1. open']),
		float(data['2. high']),
		float(data['3. low']),
		float(data['4. close']),
		float(data['5. adjusted close']),
		int(data['6. volume']),
		float(data['7. dividend amount']),
		float(data['8. split coefficient']),
		date.fromisoformat(datestr)
	)

def _map_company_overview(data: Any) -> CompanyOverview:
	return CompanyOverview(
		str(data["Symbol"]),
		str(data["AssetType"]),
		str(data["Name"]),
		str(data["Description"]),
		str(data["CIK"]),
		str(data["Exchange"]),
		str(data["Currency"]),
		str(data["Country"]),
		str(data["Sector"]),
		str(data["Industry"]),
		str(data["Address"]),
		str(data["FiscalYearEnd"]),
		date.fromisoformat(data["LatestQuarter"]),
		int(data["MarketCapitalization"]),
		int(data["EBITDA"]),
		float(data["PERatio"]),
		float(data["PEGRatio"]),
		float(data["BookValue"]),
		_safe_float(data["DividendPerShare"]),
		float(data["DividendYield"]),
		float(data["EPS"]),
		float(data["RevenuePerShareTTM"]),
		float(data["ProfitMargin"]),
		float(data["OperatingMarginTTM"]),
		float(data["ReturnOnAssetsTTM"]),
		float(data["ReturnOnEquityTTM"]),
		int(data["RevenueTTM"]),
		int(data["GrossProfitTTM"]),
		float(data["DilutedEPSTTM"]),
		float(data["QuarterlyEarningsGrowthYOY"]),
		float(data["QuarterlyRevenueGrowthYOY"]),
		float(data["AnalystTargetPrice"]),
		float(data["TrailingPE"]),
		float(data["ForwardPE"]),
		float(data["PriceToSalesRatioTTM"]),
		float(data["PriceToBookRatio"]),
		float(data["EVToRevenue"]),
		float(data["EVToEBITDA"]),
		float(data["Beta"]),
		float(data["52WeekHigh"]),
		float(data["52WeekLow"]),
		float(data["50DayMovingAverage"]),
		float(data["200DayMovingAverage"]),
		int(data["SharesOutstanding"]),
		_safe_date(data["DividendDate"]),
		_safe_date(data["ExDividendDate"])
	)

def _safe_float(value: str) -> Optional[float]:
	try:
		return float(value)
	except ValueError:
		return None

def _safe_date(value: str) -> Optional[date]:
	try:
		return date.fromisoformat(value)
	except ValueError:
		return None
