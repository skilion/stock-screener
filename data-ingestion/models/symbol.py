from dataclasses import dataclass
from datetime import datetime

@dataclass
class Symbol:
    symbol: str
    last_updated: datetime
