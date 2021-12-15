import math
import logging
from typing import Optional

import alpha_vantage
import db
import scheduler

from datetime import date, datetime

from models.datapoint import DataPoint, TimeSeries
from models.symbol import Symbol


parallel_requests = 10

async def ingest_market_data() -> None:
	today = date.today()
	symbols = db.select_symbols()
	cors = [_process_symbol(symbol) for symbol in reversed(symbols)]
	await scheduler.run_parallel(cors, parallel_requests)

async def _process_symbol(symbol: Symbol) -> None:
	if symbol.last_updated is None:
		await _download_full_timeseries(symbol)
	elif symbol.last_updated.date() == date.today():
		logging.info(f'No work needed for {symbol.symbol}')
		return
	else:
		await _download_compact_timeseries(symbol)
	logging.info(f'Downloaded overview {symbol.symbol}')
	await _download_company_overview(symbol.symbol)
	symbol.last_updated = datetime.now()
	db.update_symbol(symbol)
	logging.info(f'Done {symbol.symbol}')

async def _download_full_timeseries(symbol: Symbol) -> None:
	timeseries = await alpha_vantage.get_time_series_full(symbol.symbol)
	db.overwrite_datapoints(symbol.symbol, timeseries)

async def _download_compact_timeseries(symbol: Symbol) -> None:
	timeseries = await alpha_vantage.get_time_series_compact(symbol.symbol)
	last_datapoint_db = db.select_last_datapoint(symbol.symbol)
	last_datapoint_ts = _find_datapoint(last_datapoint_db.date_, timeseries)
	if last_datapoint_ts is None:
		await _download_full_timeseries(symbol)
		return
	same_price = math.isclose(last_datapoint_db.adjusted_close, last_datapoint_ts.adjusted_close, rel_tol=1e-3)
	if not same_price:
		# most likely a stock split has happened
		await _download_full_timeseries(symbol)
		return
	new_datapoints = filter(lambda x: x.date_ > last_datapoint_db.date_, timeseries)
	db.insert_datapoints(symbol.symbol, list(new_datapoints))

def _find_datapoint(date: date, timeseries: TimeSeries) -> Optional[DataPoint]:
	filtered = filter(lambda x: x.date_ == date, timeseries)
	filtered_list = list(filtered)
	if len(filtered_list) == 0:
		return None
	return filtered_list[0]

async def _download_company_overview(symbol: str) -> None:
	overview = await alpha_vantage.get_company_overview(symbol)
	db.delete_company_overview(symbol)
	db.insert_company_overview(overview)
