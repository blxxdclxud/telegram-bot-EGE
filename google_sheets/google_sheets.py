from data.config import logger, CREDENTIALS_FILE, SPREADSHEET_ID
import os
import sys
import traceback

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
http_auth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=http_auth)


def fill_whole_table(data):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"A9:N{8 + len(data)}",
                 "majorDimension": "ROWS",
                 "values": data}
            ]
        }).execute()


def start_spreadsheet():
    user_data = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        majorDimension="ROWS",
        range="B4:B6"
    ).execute()["values"][0]

    logger.info(f'{__name__}/{sys._getframe().f_code.co_name}')
