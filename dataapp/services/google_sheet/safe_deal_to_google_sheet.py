import redis
import time
import json

from pprint import pprint
from datetime import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


MONTH_NAME_LIST = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

CREDENTIALS_FILE = "creds.json"
# SPREADSHEET_ID = '1eweIL3uEzJAcNK5K1QYkKpUoOPfFhbY-4bP38jaicp0'
SPREADSHEET_ID = "1sM2AweePLayksP2f_dwabT9-ZNO6CovfCTrwlV31rP4"

SHEET_NUMBER = 0            # Порядковый номер листа (нумерация начинается с 0)
COL_NAME_WITH_IDS = "A"     # Название столбца где хранятся ID сделок для поиска дублей
# Столбец с которого обновляются данные, если сделка уже есть в БД
COL_WITH_START_UPDATE = {
    "name": "E",
    "number": 5
}

class GoogleAPI:
    def __init__(self, spreadsheet_id, credentials_file):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.client = None

    def connect(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )
        httpAuth = credentials.authorize(httplib2.Http())
        self.client = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def get_sheet_name(self, sheet_num):
        sheet_metadata = self.client.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        sheet_name = sheets[sheet_num]['properties']['title']
        return sheet_name

    def get_data_column(self, sheet_name, col_name):
        request = self.client.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!{col_name}:{col_name}",
            majorDimension='COLUMNS'
        )
        response = request.execute()
        return response.get("values", [None,])[0]

    def append_row(self, sheet_name, row_index, data):
        # request = self.client.spreadsheets().values().update(
        #     spreadsheetId=self.spreadsheet_id,
        #     range=f'{sheet_name}!A{row_index}',
        #     valueInputOption='RAW',
        #     body={'values': [data,]}
        # )
        request = self.client.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_name,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={
                'values': [data],
            },
        )
        response = request.execute()
        return response

    def update_row(self, sheet_name, start_col_name, row_index, data):
        request = self.client.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f'{sheet_name}!{start_col_name}{row_index}',
            valueInputOption='USER_ENTERED',
            body={'values': [data,]}
        )
        response = request.execute()
        return response

    def remove_row(self, sheet_id, row_index):
        delete_request = {
            "deleteDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": row_index,
                    "endIndex": row_index + 1
                }
            }
        }
        request = self.client.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={"requests": [delete_request]}
        )
        response = request.execute()
        return response


def find_index(lst, item):
    try:
        index = lst.index(item)
    except ValueError:
        index = None
    return index


def get_month(date_obj):
    if date_obj:
        month = date_obj.month
        return MONTH_NAME_LIST[month - 1]
    else:
        return ""


def get_payment(paymentRub):
    if paymentRub:
        return float(paymentRub.split("|")[0])
    else:
        return 0


def getDirection(direction):
    newDir = ""
    if direction:
        newDir = direction.replace(" по ОТ(повторный)", "")
    return newDir


def date_parser(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    except (ValueError, TypeError):
        date_obj = None
    return date_obj


def get_row_for_insert_to_google(deal):
    date_obj_start_work = date_parser(deal.get("UF_CRM_WORK_ACCEPTENCE_DAY"))
    date_obj_payment = date_parser(deal.get("UF_CRM_1553188396"))
    date_obj_delivery = date_parser(deal.get("UF_CRM_1540262622"))
    date_obj_act = date_parser(deal.get("UF_CRM_1572403036"))
    date_obj_contract_deadline = date_parser(deal.get("UF_CRM_1526281552"))
    date_obj_expected_payment = date_parser(deal.get("UF_CRM_1676966362"))

    direction = getDirection(deal.get("direction"))
    if deal.get("UF_CRM_1611128441") == "Оценка проф. рисков":
        direction = "Оценка проф. рисков"
    if deal.get("UF_CRM_1611128441") == "Программа ПК":
        direction = "ПК"
    if deal.get("UF_CRM_1611128441") == "Аутсорсинг":
        direction = "Охрана труда"

    return [
        int(deal.get('ID')),
        date_obj_start_work.year if date_obj_start_work else "",
        get_month(date_obj_start_work) or "",
        date_obj_start_work.strftime('%d.%m.%Y') if date_obj_start_work else "",
        deal.get("company") or "",
        deal.get("assigned") or "",
        deal.get("rop") or "",
        f"https://atonlab.bitrix24.ru/crm/deal/details/{deal.get('ID')}/",
        float(deal.get("UF_CRM_1619591604401")) if deal.get("UF_CRM_1619591604401") else 0,
        get_payment(deal.get("UF_CRM_1575375338"))  or 0,
        date_obj_payment.strftime("%d.%m.%Y") if date_obj_payment else "",
        float(deal.get("UF_CRM_1620264903")) if deal.get("UF_CRM_1620264903") else 0,
        direction or "",                              # направление
        deal.get("UF_CRM_1611128441") or "",          # услуга
        deal.get("UF_CRM_1611202566") or "",          # инженер
        date_obj_delivery.strftime("%d.%m.%Y") if date_obj_delivery else "",
        deal.get("UF_CRM_1581493417") or "",
        date_obj_act.strftime("%d.%m.%Y") if date_obj_act else "",
        deal.get("stage") or "",
        deal.get("source") or "",
        deal.get("source_dir") or "",
        # deal.get("source_id"),
        deal.get("UF_CRM_1681619452562") or "",
        deal.get("UTM_SOURCE") or "",
        deal.get("UTM_CAMPAIGN") or "",
        deal.get("crm_status") or "",
        deal.get("pb_out") or "",
        date_obj_contract_deadline.strftime("%d.%m.%Y") if date_obj_contract_deadline else "",
        date_obj_expected_payment.strftime("%d.%m.%Y") if date_obj_expected_payment else "",
        # deal.get("UF_CRM_1602484766")
    ]


def add_deal_to_google(deal):
    api = GoogleAPI(SPREADSHEET_ID, CREDENTIALS_FILE)
    api.connect()
    sheet_name = api.get_sheet_name(SHEET_NUMBER)
    ids_deals = api.get_data_column(sheet_name, COL_NAME_WITH_IDS)
    row = find_index(ids_deals, deal["ID"])
    data = get_row_for_insert_to_google(deal)

    if deal["deal_won"] and row:
        ind_start_slice = COL_WITH_START_UPDATE["number"] - 1
        api.update_row(sheet_name, COL_WITH_START_UPDATE["name"], row + 1, data[ind_start_slice:])

        api.append_row("log", len(api.get_data_column("log", COL_NAME_WITH_IDS)) + 1, [data[0], "UPDATE", deal.get("UF_CRM_1602484766"), json.dumps(deal, ensure_ascii=False), json.dumps(data, ensure_ascii=False)])
    elif not deal["deal_won"] and row:
        api.remove_row(SHEET_NUMBER, row)

        api.append_row("log", len(api.get_data_column("log", COL_NAME_WITH_IDS)) + 1, [data[0], "REMOVE", deal.get("UF_CRM_1602484766"), json.dumps(deal, ensure_ascii=False), json.dumps(data, ensure_ascii=False)])
    elif deal["deal_won"] and deal.get("UF_CRM_1602484766") == "5":
        api.append_row(sheet_name, len(ids_deals) + 1, data)

        api.append_row("log", len(api.get_data_column("log", COL_NAME_WITH_IDS)) + 1, [data[0], "APPEND", deal.get("UF_CRM_1602484766"), json.dumps(deal, ensure_ascii=False), json.dumps(data, ensure_ascii=False)])


def run():
    redis_client = redis.Redis(host='localhost', port=6379, db=5)

    while True:
        try:
            if redis_client.ping():
                pass
                # print('Соединение с Redis восстановлено')
            else:
                print('Нет связи с Redis')
        except redis.exceptions.ConnectionError:
            print('Потеряно соединение с Redis. Переподключение...')
            time.sleep(5)
            continue

        queue_item = redis_client.blpop("googlequeue", timeout=60)
        if queue_item:
            deal_str = queue_item[1].decode('utf-8')
            deal = json.loads(deal_str)
            add_deal_to_google(deal)

        time.sleep(1)


if __name__ == "__main__":
    run()
