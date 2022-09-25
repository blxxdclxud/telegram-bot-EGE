import logging
from json import load, dump
import os


def get_json_data():
    global TABLE_DATA
    with open(TABLE_DATA_FILE, 'r') as file:
        TABLE_DATA = load(file)


def update_json_data(data):
    with open(TABLE_DATA_FILE, 'w') as file:
        dump(data, file)
        # print(data)
    get_json_data()


CREDENTIALS_FILE = os.path.abspath("./data/creds.json")
SPREADSHEET_ID = "10CjeiyEPr8R1SVOl5V0vbKMd3RRg4LQq7MVIIlDb0m0"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=os.path.abspath("./logs/bot.log"))
logger = logging.getLogger(__name__)

TABLE_DATA_FILE = os.path.abspath("./data/table_data.json")

TABLE_DATA = None

PERSONAL_SHEET_ID = 1768054183
GENERAL_SHEET_ID = 922424769
