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
	ebitda: Optional[int]
	pe_ratio: Optional[float]
	peg_ratio: Optional[float]
	book_value: Optional[float]
	dividend_per_share: Optional[float]
	dividend_yield: Optional[float]
	eps: Optional[float]
	revenue_per_share_ttm: Optional[float]
	profit_margin: Optional[float]
	operating_margin_ttm: Optional[float]
	return_on_assets_ttm: Optional[float]
	return_on_equity_ttm: Optional[float]
	revenue_ttm: Optional[int]
	gross_profit_ttm: Optional[int]
	diluted_eps_ttm: Optional[float]
	quarterly_earnings_growth_yoy: Optional[float]
	quarterly_revenue_growth_yoy: Optional[float]
	analyst_target_price: Optional[float]
	trailing_pe: Optional[float]
	forward_pe: Optional[float]
	price_to_sales_ratio_ttm: Optional[float]
	price_to_book_ratio: Optional[float]
	ev_to_revenue: Optional[float]
	ev_to_ebitda: Optional[float]
	beta: Optional[float]
	high_52_week: Optional[float]
	low_52_week: Optional[float]
	moving_average_50_day: Optional[float]
	moving_average_200_day: Optional[float]
	shares_outstanding: Optional[int]
	dividend_date: Optional[date]
	ex_dividend_date: Optional[date]
