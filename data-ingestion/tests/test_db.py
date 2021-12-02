import unittest
from datetime import date, datetime

import db
from models import CompanyOverview, DataPoint, Symbol, TimeSeries

class TestDb(unittest.TestCase):
	testSymbol = 'TEST'

	def setUp(self):
		self.cleanup()

	def tearDown(self):
		self.cleanup()

	def test_select_symbols(self):
		# Arrange
		self.insert_test_symbol()

		# Act
		results = db.select_symbols()

		# Assert
		symbol: Symbol = next(filter(lambda x: x.symbol == self.testSymbol, results))
		assert (symbol.last_updated is None)

	def test_update_symbol(self):
		# Arrange
		self.insert_test_symbol()
		updated_symbol = Symbol(self.testSymbol, datetime(2021, 12, 2))

		# Act
		db.update_symbol(updated_symbol)

		# Assert
		cursor = db._connection.execute('SELECT LastUpdated FROM Symbol WHERE Symbol = ?', self.testSymbol)
		last_date = cursor.fetchone()
		assert last_date.LastUpdated == updated_symbol.last_updated

	def test_select_last_datapoint(self):
		# Arrange
		last_date = date(2021, 12, 2)
		last_price = 2
		self.insert_test_symbol()
		self.insert_test_price(date(2021, 12, 1), 1)
		self.insert_test_price(last_date, last_price)

		# Act
		result = db.select_last_datapoint(self.testSymbol)

		# Assert
		assert result.date_ == last_date
		assert result.adjusted_close == last_price

	def test_delete_datapoints(self):
		# Arrange
		self.insert_test_symbol()
		self.insert_test_price(date(2021, 12, 2), 1)

		# Act
		db.delete_datapoints(self.testSymbol)

		# Assert
		assert self.count_datapoints() == 0

	def test_insert_datapoints(self):
		# Arrange
		self.insert_test_symbol()
		datapoint1 = DataPoint(0, 0, 0, 0, 0, 0, 0, 0, date(2021, 12, 1))
		datapoint2 = DataPoint(0, 0, 0, 0, 0, 0, 0, 0, date(2021, 12, 2))

		# Act
		db.insert_datapoints(self.testSymbol, [datapoint1, datapoint2])

		# Assert
		assert self.count_datapoints() == 2

	def insert_test_symbol(self):
		cursor = db._connection.execute('INSERT INTO Symbol (Symbol) VALUES (?)', self.testSymbol)
		cursor.commit()

	def insert_test_price(self, date: date, adjustedClose: float):
		sql = '''
			INSERT INTO DataPoint (Symbol, Date, [Open], High, Low, [Close],
            	AdjustedClose, Volume, DividendAmount, SplitCoefficient)
        	VALUES (?, ?, 0, 0, 0, 0, ?, 0, 0, 0)
		'''
		cursor = db._connection.execute(sql, self.testSymbol, date, adjustedClose)
		cursor.commit()

	def count_datapoints(self) -> int:
		cursor = db._connection.execute('SELECT COUNT(1) FROM DataPoint WHERE Symbol = ?', self.testSymbol)
		count = cursor.fetchone()[0]
		return count

	def cleanup(self):
		cursor = db._connection.cursor()
		cursor.execute(f'DELETE FROM DataPoint WHERE Symbol = ?', self.testSymbol)
		cursor.execute(f'DELETE FROM CompanyOverview WHERE Symbol = ?', self.testSymbol)
		cursor.execute(f'DELETE FROM Symbol WHERE Symbol = ?', self.testSymbol)
		cursor.commit()
