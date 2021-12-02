import pyodbc
import config

connection = pyodbc.connect(config.odbc_connection_string)

def get_symbols() -> list[str]:
    sql = "SELECT * FROM Symbol"
    cursor = connection.execute(sql)
    return list(map(lambda x: x.Symbol, cursor.fetchall()))