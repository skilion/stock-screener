# Data Ingestion

Azure function to import prices and static data from Alpha Vantage.
Runs automatically after US market close (22:00 UTC).

## Usage

1. Edit `local.settings.json.default` and rename it to `local.settings.json`
2. Deploy `func azure functionapp publish <FunctionAppName>`
