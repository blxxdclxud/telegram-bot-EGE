import logging

CREDENTIALS_FILE = "creds.json"
SPREADSHEET_ID = "1VUUwcSYO0P8vBe3iFbS0SfNswKBgK2e6"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='./logs/bot.log')
logger = logging.getLogger(__name__)
