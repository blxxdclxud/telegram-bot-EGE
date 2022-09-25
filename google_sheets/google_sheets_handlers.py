from data.config import logger, CREDENTIALS_FILE, SPREADSHEET_ID, update_json_data, \
    get_json_data, GENERAL_SHEET_ID, PERSONAL_SHEET_ID
import data.config as cfg

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


def next_available_row(worksheet):
    str_list = filter(None, worksheet.col_values(1))
    return str(len(str_list) + 1)


get_json_data()

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
http_auth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=http_auth)


def copy_sheet(_from, _to):
    request = [{
        "copyPaste": {
            "source": {
                "sheetId": _from,
                "startRowIndex": 0,
                "startColumnIndex": 0,
            },
            "destination": {
                "sheetId": _to,
                "startRowIndex": 0,
                "startColumnIndex": 0,
            },
            "pasteType": "PASTE_NORMAL",
            "pasteOrientation": "NORMAL"
        }},
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": _to,
                    "dimension": "COLUMNS",
                    "startIndex": 1,
                    "endIndex": 19
                },
                "properties": {
                    "pixelSize": 45
                },
                "fields": "pixelSize"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": _to,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 1
                },
                "properties": {
                    "pixelSize": 176
                },
                "fields": "pixelSize"
            }
        }
    ]

    response = service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            'requests': request
        }).execute()


def add_data_to_general_table(data, variant, sheets_names):
    _name = data["name"]
    sheet_name = data["grade"] + " Вариант " + str(variant)

    if sheet_name not in sheets_names:
        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]

        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'requests': requests
            }).execute()

        cfg.TABLE_DATA["general"][sheet_name] = {
            "last_filled_row": 2,
            "variant": variant
        }
        update_json_data(cfg.TABLE_DATA)

        copy_sheet(GENERAL_SHEET_ID, response["replies"][0]["addSheet"]["properties"]["sheetId"])

    first_blank_row = cfg.TABLE_DATA["general"][sheet_name]["last_filled_row"] + 1

    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{sheet_name}!A{first_blank_row}:S{first_blank_row}",
                 "majorDimension": "ROWS",
                 "values": [[_name] + list(data.values())[2:]]}
            ]
        }).execute()

    cfg.TABLE_DATA["general"][sheet_name]["last_filled_row"] += 1


def add_data_to_personal_table(data):
    _name = data["name"]

    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheets_names = [sheet["properties"]["title"] for sheet in sheets]
    # print(sheets)

    if _name not in sheets_names:
        requests = [{
            'addSheet': {
                'properties': {
                    'title': _name
                }
            }
        }]

        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={
                'requests': requests
            }).execute()

        copy_sheet(PERSONAL_SHEET_ID, response["replies"][0]["addSheet"]["properties"]["sheetId"])

        cfg.TABLE_DATA["personal"][_name] = {
            "last_filled_row": 2,
            "last_variant": 0
        }
        update_json_data(cfg.TABLE_DATA)

    first_blank_row = cfg.TABLE_DATA["personal"][_name]["last_filled_row"] + 1
    _variant = cfg.TABLE_DATA["personal"][_name]["last_variant"] + 1

    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{_name}!A{first_blank_row}:S{first_blank_row}",
                 "majorDimension": "ROWS",
                 "values": [[_variant] + list(data.values())[2:]]}
            ]
        }).execute()

    cfg.TABLE_DATA["personal"][_name]["last_filled_row"] += 1
    cfg.TABLE_DATA["personal"][_name]["last_variant"] += 1

    add_data_to_general_table(data, _variant, sheets_names)

    update_json_data(cfg.TABLE_DATA)


# for i in ({"name": "Назмиев Рамазан",
#            "grade": "11А",
#            1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2,
#            9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2,
#            17: 2, 18: 2},
#           {"name": "Fc VV",
#            "grade": "11А",
#            1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2,
#            9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2,
#            17: 2, 18: 2},
#           {"name": "FF cww",
#            "grade": "11Б",
#            1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2,
#            9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2,
#            17: 2, 18: 2},
#           {"name": "Назмиев Рамазан",
#            "grade": "11А",
#            1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2,
#            9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2,
#            17: 2, 18: 2}):
#     add_data_to_personal_table(i)
