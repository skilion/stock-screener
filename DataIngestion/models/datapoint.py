from dataclasses import dataclass
from datetime import date

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

TimeSeries = list[DataPoint]
