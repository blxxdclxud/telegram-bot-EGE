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
with open(os.path.abspath("./data/config.txt")) as cfg_file:
    data = cfg_file.readlines()
    SPREADSHEET_ID = data[0].strip().split("=")[-1]
    PERSONAL_SHEET_ID = int(data[1].strip().split("=")[-1])
    GENERAL_SHEET_ID = int(data[2].strip().split("=")[-1])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=os.path.abspath("./logs/bot.log"))
logger = logging.getLogger(__name__)

TABLE_DATA_FILE = os.path.abspath("./data/table_data.json")

TABLE_DATA = None

__secret = "{__name__}/{sys._getframe().f_code.co_name}"
