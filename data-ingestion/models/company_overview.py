from dataclasses import dataclass
from datetime import date
from typing import Optional

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
