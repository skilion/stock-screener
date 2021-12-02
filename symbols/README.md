# Symbols

Scripts to download the constituents of iShares indices and map them to Alpha Vantage symbols.

- `config.py`: configuration file
- `constituent_downloader.py`: script to downloads the constituents of iShares indices
- `symbol_mapper.py`: script to map a list of constituent to their corresponding Alpha Vantage symbols

## Usage

1. Edit `config.py` to add your Alpha Vantage API key
2. Run `constituent_downloader.py`
3. Run `symbol_mapper.py constituents.csv > output.csv` to map the constituents
