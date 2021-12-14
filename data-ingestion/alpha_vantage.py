import httpx
import logging
import random
import time
from datetime import date
from typing import Any, Optional

import config
from models import CompanyOverview, DataPoint, TimeSeries

_client = httpx.AsyncClient()

async def get_time_series_compact(symbol: str) -> TimeSeries:
	logging.debug(f'get_time_series_compact {symbol}')
	return await _request_time_series(symbol, False)

async def get_time_series_full(symbol: str) -> TimeSeries:
	logging.debug(f'get_time_series_full {symbol}')
	return await _request_time_series(symbol, True)

async def get_company_overview(symbol: str) -> CompanyOverview:
	logging.debug(f'get_company_overview {symbol}')
	payload = {
		'function': 'OVERVIEW',
		'symbol': symbol,
		'apikey': config.alpha_vantage_api_key
	}
	data = await _make_request(payload)
	if 'Symbol' not in data:
		logging.error(f'Unexpected data format {data}')
		raise Exception('get_company_overview failed')
	return _map_company_overview(data)

async def _request_time_series(symbol: str, full: bool) -> TimeSeries:
	payload = {
		'function': 'TIME_SERIES_DAILY_ADJUSTED',
		'symbol': symbol,
		'outputsize': 'full' if full else 'compact',
		'apikey': config.alpha_vantage_api_key
	}
	data = await _make_request(payload)
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

async def _make_request(payload: Any) -> Any:
	data = {}
	for _ in range(3):
		data = (await _make_http_request(payload)).json()
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

async def _make_http_request(payload: Any) -> httpx.Response:
	retry = 3
	while True:
		try:
			response = await _client.get('https://www.alphavantage.co/query', params=payload)
			response.raise_for_status()
			return response
		except httpx.HTTPError as e:
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
		_safe_int(data["EBITDA"]),
		_safe_float(data["PERatio"]),
		_safe_float(data["PEGRatio"]),
		_safe_float(data["BookValue"]),
		_safe_float(data["DividendPerShare"]),
		_safe_float(data["DividendYield"]),
		_safe_float(data["EPS"]),
		_safe_float(data["RevenuePerShareTTM"]),
		_safe_float(data["ProfitMargin"]),
		_safe_float(data["OperatingMarginTTM"]),
		_safe_float(data["ReturnOnAssetsTTM"]),
		_safe_float(data["ReturnOnEquityTTM"]),
		_safe_int(data["RevenueTTM"]),
		_safe_int(data["GrossProfitTTM"]),
		_safe_float(data["DilutedEPSTTM"]),
		_safe_float(data["QuarterlyEarningsGrowthYOY"]),
		_safe_float(data["QuarterlyRevenueGrowthYOY"]),
		_safe_float(data["AnalystTargetPrice"]),
		_safe_float(data["TrailingPE"]),
		_safe_float(data["ForwardPE"]),
		_safe_float(data["PriceToSalesRatioTTM"]),
		_safe_float(data["PriceToBookRatio"]),
		_safe_float(data["EVToRevenue"]),
		_safe_float(data["EVToEBITDA"]),
		_safe_float(data["Beta"]),
		_safe_float(data["52WeekHigh"]),
		_safe_float(data["52WeekLow"]),
		_safe_float(data["50DayMovingAverage"]),
		_safe_float(data["200DayMovingAverage"]),
		_safe_int(data["SharesOutstanding"]),
		_safe_date(data["DividendDate"]),
		_safe_date(data["ExDividendDate"])
	)

def _safe_date(value: str) -> Optional[date]:
	try:
		return date.fromisoformat(value)
	except ValueError:
		return None

def _safe_float(value: str) -> Optional[float]:
	try:
		return float(value)
	except ValueError:
		return None

def _safe_int(value: str) -> Optional[int]:
	try:
		return int(value)
	except ValueError:
		return None
