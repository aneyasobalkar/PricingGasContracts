import logging
from datetime import datetime
class Logger:
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=f'Logs/{datetime.now()}.log', encoding='utf-8', level=logging.INFO)