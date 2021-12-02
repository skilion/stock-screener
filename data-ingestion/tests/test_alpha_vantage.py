import unittest

import alpha_vantage

class TestAlphaVantage(unittest.TestCase):
    def test_get_time_series_compact(self):
        # Arrange
        symbol = 'TSLA'

        # Act
        time_series = alpha_vantage.get_time_series_compact(symbol)

        # Assert
        assert len(time_series) == 100
        assert time_series[0].adjusted_close < time_series[-1].adjusted_close
        TestAlphaVantage.assert_time_series_is_valid(time_series)

    def test_get_time_series_full(self):
        # Arrange
        symbol = 'TSLA'

        # Act
        time_series = alpha_vantage.get_time_series_full(symbol)

        # Assert
        assert len(time_series) > 200
        assert time_series[0].adjusted_close < time_series[-1].adjusted_close
        TestAlphaVantage.assert_time_series_is_valid(time_series)

    def test_get_company_overview(self):
        # Arrange
        symbol = 'TSLA'

        # Act
        overview = alpha_vantage.get_company_overview(symbol)

        # Assert
        assert overview.symbol == symbol
        assert overview.shares_outstanding > 0

    @staticmethod
    def assert_time_series_is_valid(time_series: alpha_vantage.TimeSeries):
        for i in range(len(time_series) - 1):
            assert time_series[i].open > 0
            assert time_series[i].close > 0
            assert time_series[i].high > 0
            assert time_series[i].low > 0
            assert time_series[i].adjusted_close > 0
            assert time_series[i].split_coefficient > 0
            assert time_series[i].dividend_amount >= 0
            assert time_series[i].volume > 0
            assert time_series[i].date_ < time_series[i + 1].date_, 'timeseries not in ascending ordered'
