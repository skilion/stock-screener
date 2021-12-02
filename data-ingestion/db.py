import pyodbc
from itertools import chain
from typing import Any

import config
from models import CompanyOverview, DataPoint, Symbol, TimeSeries

_connection = pyodbc.connect(config.odbc_connection_string)

def select_symbols() -> list[Symbol]:
    sql = 'SELECT Symbol, LastUpdated FROM Symbol'
    cursor = _connection.execute(sql)
    return list(map(lambda x: _map_symbol(x), cursor.fetchall()))

def update_symbol(symbol: Symbol) -> None:
    sql = 'UPDATE Symbol SET LastUpdated = ? WHERE Symbol = ?'
    cursor = _connection.execute(sql, symbol.last_updated, symbol.symbol)
    cursor.commit()

def select_last_datapoint(symbol: str) -> DataPoint:
    sql = '''
        SELECT Symbol, Date, [Open], High, Low, [Close], AdjustedClose,
            Volume, DividendAmount, SplitCoefficient
        FROM DataPoint
        WHERE Symbol = ? AND Date = (
            SELECT MAX(Date)
            FROM DataPoint
            WHERE Symbol = ?
        )
        '''
    cursor = _connection.execute(sql, symbol, symbol)
    return _map_datapoint(cursor.fetchone())

def delete_datapoints(symbol: str) -> None:
    sql = 'DELETE FROM DataPoint WHERE Symbol = ?'
    cursor = _connection.execute(sql, symbol)
    cursor.commit()

def insert_datapoints(symbol: str, datapoints: TimeSeries) -> None:
    sql = '''
        INSERT INTO DataPoint (Symbol, Date, [Open], High, Low, [Close],
            AdjustedClose, Volume, DividendAmount, SplitCoefficient)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor = _connection.cursor()
    cursor.fast_executemany = True
    cursor.executemany(sql, map(lambda x: list(chain([symbol], _unmap_datapoint(x))), datapoints))
    cursor.commit()

def delete_company_overview(symbol: str) -> None:
    sql = 'DELETE FROM CompanyOverview WHERE Symbol = ?'
    cursor = _connection.execute(sql, symbol)
    cursor.commit()

def insert_company_overview(overview: CompanyOverview) -> None:
    sql = '''
        INSERT INTO CompanyOverview (Symbol, AssetType, Name, Description, CIK,
            Exchange, Currency, Country, Sector, Industry, Address,
            FiscalYearEnd, LatestQuarter, MarketCapitalization, EBITDA,
            PERatio, PEGRatio, BookValue, DividendPerShare, DividendYield, EPS,
            RevenuePerShareTTM, ProfitMargin, OperatingMarginTTM,
            ReturnOnAssetsTTM, ReturnOnEquityTTM, RevenueTTM, GrossProfitTTM,
            DilutedEPSTTM, QuarterlyEarningsGrowthYOY,
            QuarterlyRevenueGrowthYOY, AnalystTargetPrice, TrailingPE,
            ForwardPE, PriceToSalesRatioTTM, PriceToBookRatio, EVToRevenue,
            EVToEBITDA, Beta, [52WeekHigh], [52WeekLow], [50DayMovingAverage],
            [200DayMovingAverage], SharesOutstanding, DividendDate,
            ExDividendDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?)
    '''
    cursor =_connection.execute(sql, _unmap_company_verview(overview))
    cursor.commit()

def _map_symbol(row: pyodbc.Row) -> Symbol:
    return Symbol(
        row.Symbol,
        row.LastUpdated
    )

def _map_datapoint(row: pyodbc.Row) -> DataPoint:
    return DataPoint(
        row.Open,
        row.High,
        row.Low,
        row.Close,
        row.AdjustedClose,
        row.Volume,
        row.DividendAmount,
        row.SplitCoefficient,
        row.Date,
    )

def _unmap_datapoint(datapoint: DataPoint) -> list[Any]:
    return [
        datapoint.date_,
        datapoint.open,
        datapoint.high,
        datapoint.low,
        datapoint.close,
        datapoint.adjusted_close,
        datapoint.volume,
        datapoint.dividend_amount,
        datapoint.split_coefficient
    ]

def _unmap_company_verview(overview: CompanyOverview) -> list[Any]:
    return [
        overview.symbol,
        overview.asset_type,
        overview.name,
        overview.description,
        overview.cik,
        overview.exchange,
        overview.currency,
        overview.country,
        overview.sector,
        overview.industry,
        overview.address,
        overview.fiscal_year_end,
        overview.latest_quarter,
        overview.market_capitalization,
        overview.ebitda,
        overview.pe_ratio,
        overview.peg_ratio,
        overview.book_value,
        overview.dividend_per_share,
        overview.dividend_yield,
        overview.eps,
        overview.revenue_per_share_ttm,
        overview.profit_margin,
        overview.operating_margin_ttm,
        overview.return_on_assets_ttm,
        overview.return_on_equity_ttm,
        overview.revenue_ttm,
        overview.gross_profit_ttm,
        overview.diluted_eps_ttm,
        overview.quarterly_earnings_growth_yoy,
        overview.quarterly_revenue_growth_yoy,
        overview.analyst_target_price,
        overview.trailing_pe,
        overview.forward_pe,
        overview.price_to_sales_ratio_ttm,
        overview.price_to_book_ratio,
        overview.ev_to_revenue,
        overview.ev_to_ebitda,
        overview.beta,
        overview.high_52_week,
        overview.low_52_week,
        overview.moving_average_50_day,
        overview.moving_average_200_day,
        overview.shares_outstanding,
        overview.dividend_date,
        overview.ex_dividend_date
    ]
