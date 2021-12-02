import logging
import random
import requests
import time
from typing import Any, Optional
from dataclasses import dataclass
from datetime import date, timedelta

import config

@dataclass
class DataPoint:
	open: float
	high: float
	low: float
	close: float
	adjusted_close: float
	volume: int
	dividend_amount: float
	split_coefficient: float
	date_: date

	@staticmethod
	def make(datestr: str, data: Any):
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

TimeSeries = list[DataPoint]

@dataclass
class CompanyOverview:
	symbol: str
	asset_type: str
	name: str
	description: str
	cik: str
	exchange: str
	currency: str
	country: str
	sector: str
	industry: str
	address: str
	fiscal_year_end: str
	latest_quarter: date
	market_capitalization: int
	ebitda: int
	pe_ratio: float
	peg_ratio: float
	book_value: float
	dividend_per_share: Optional[float]
	dividend_yield: float
	eps: float
	revenue_per_share_ttm: float
	profit_margin: float
	operating_margin_ttm: float
	return_on_assets_ttm: float
	return_on_equity_ttm: float
	revenue_ttm: int
	gross_profit_ttm: int
	diluted_eps_ttm: float
	quarterly_earnings_growth_yoy: float
	quarterly_revenue_growth_yoy: float
	analyst_target_price: float
	trailing_pe: float
	forward_pe: float
	price_to_sales_ratio_ttm: float
	price_to_book_ratio: float
	ev_to_revenue: float
	ev_to_ebitda: float
	beta: float
	high_52_week: float
	low_52_week: float
	moving_average_50_day: float
	moving_average_200_day: float
	shares_outstanding: int
	dividend_date: Optional[date]
	ex_dividend_date: Optional[date]

	@staticmethod
	def make(data: Any):
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
	return CompanyOverview.make(data)

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
	timeseries = list(map(lambda x: DataPoint.make(*x), time_series.items()))
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
