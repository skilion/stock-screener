# Data Ingestion

Azure function to import prices and static data from Alpha Vantage. Runs automatically after US market close (22:00 UTC)

## Usage

1. Edit `config.py.default` and rename it to `config.py`
2. Deploy `func azure functionapp publish <FunctionAppName>`
