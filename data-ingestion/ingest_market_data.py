import math
import logging
from typing import Optional

import alpha_vantage
import db

from datetime import date, datetime

from models.datapoint import DataPoint, TimeSeries
from models.symbol import Symbol

def ingest_market_data() -> None:
    today = date.today()
    symbols = db.select_symbols()
    for symbol in symbols:
        logging.info(f'Processing {symbol.symbol}')
        if symbol.last_updated is None:
            _download_full_timeseries(symbol)
        elif symbol.last_updated.date() == today:
            logging.info(f'Already updated today')
            continue
        else:
            _download_compact_timeseries(symbol)
        _download_company_overview(symbol.symbol)
        symbol.last_updated = datetime.now()
        db.update_symbol(symbol)

def _download_full_timeseries(symbol: Symbol) -> None:
    timeseries = alpha_vantage.get_time_series_full(symbol.symbol)
    db.delete_datapoints(symbol.symbol)
    db.insert_datapoints(symbol.symbol, timeseries)

def _download_compact_timeseries(symbol: Symbol) -> None:
    timeseries = alpha_vantage.get_time_series_compact(symbol.symbol)
    last_datapoint_db = db.select_last_datapoint(symbol.symbol)
    last_datapoint_ts = _find_datapoint(last_datapoint_db.date_, timeseries)
    if last_datapoint_ts is None:
        _download_full_timeseries(symbol)
        return
    same_price = math.isclose(last_datapoint_db.adjusted_close, last_datapoint_ts.adjusted_close, rel_tol=1e-3)
    if not same_price:
        # most likely a stock split has happened
        _download_full_timeseries(symbol)
        return
    new_datapoints = filter(lambda x: x.date_ > last_datapoint_db.date_, timeseries)
    db.insert_datapoints(symbol.symbol, list(new_datapoints))

def _find_datapoint(date: date, timeseries: TimeSeries) -> Optional[DataPoint]:
    filtered = filter(lambda x: x.date_ == date, timeseries)
    filtered_list = list(filtered)
    if len(filtered_list) == 0:
        return None
    return filtered_list[0]

def _download_company_overview(symbol: str) -> None:
    overview = alpha_vantage.get_company_overview(symbol)
    db.delete_company_overview(symbol)
    db.insert_company_overview(overview)
