import datetime
import logging

import azure.functions as func
import ingest_market_data

async def main(mytimer: func.TimerRequest) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if mytimer.past_due:
        logging.info('The timer is past due!')

    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    await ingest_market_data.ingest_market_data()
