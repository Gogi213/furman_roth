import calendar
from datetime import datetime


def get_unique_values(service, spreadsheet_id, range):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    values = result.get('values', [])

    # Извлечение уникальных значений из первого столбца, начиная со второй строки (исключая заголовок)
    unique_values = list({row[0] for row in values[1:] if row})  # Пропускаем первую строку
    return unique_values

def create_creative_reports_sheets(service, spreadsheet_id, names):
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    existing_sheets = [sheet['properties']['title'] for sheet in sheet_metadata.get('sheets', [])]

    headers = ["Advertiser + Campaign", "Advertiser", "Campaign", "Tactic", "Date", "Ad Size", "Impressions", "Clicks", "CTR", "PCC", "PVC"]

    for name in names:
        sheet_name = f"{name}_creatives"
        if name and sheet_name not in existing_sheets:
            create_sheet_request = {
                'requests': [{'addSheet': {'properties': {'title': sheet_name}}}]
            }
            service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=create_sheet_request).execute()

            header_range = f"{sheet_name}!A1:K1"
            value_range_body = {"values": [headers]}
            service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=header_range, valueInputOption="RAW", body=value_range_body).execute()

            print(f'Sheet "{sheet_name}" created with headers.')
        else:
            print(f'Sheet "{sheet_name}" already exists or name is invalid.')


def get_fact_data(service, spreadsheet_id):
    range = 'fact!A:F'  # Диапазон A-F для извлечения текстовых и числовых данных
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    values = result.get('values', [])

    # Извлечение данных, пропускаем заголовок
    fact_data = [row for row in values[1:] if row]
    return fact_data

def get_dates_for_current_month():
    year, month = datetime.now().year, datetime.now().month
    num_days = calendar.monthrange(year, month)[1]
    return [datetime(year, month, day).strftime("%Y-%m-%d") for day in range(1, num_days + 1)]


def update_creative_sheets_with_dates(service, spreadsheet_id, sheet_name, fact_data):
    dates = get_dates_for_current_month()
    campaign_name = sheet_name.replace('_creatives', '')
    ad_sizes = get_ad_sizes_for_campaign(service, spreadsheet_id, campaign_name)

    # Словарь для хранения данных по кампании (ключ - название кампании)
    campaign_info = {row[0]: row[1:4] for row in fact_data if row[0].startswith(campaign_name)}

    values = []
    for ad_size in ad_sizes:
        # Если есть информация о кампании, используем ее, иначе оставляем пустыми
        advertiser, campaign, tactic = campaign_info.get(campaign_name, ['', '', ''])
        for date in dates:
            # Для каждой даты и каждого Ad Size создаем строку с информацией о кампании
            row = [campaign_name, advertiser, campaign, tactic, date, ad_size, '', '', '', '', '']
            values.append(row)

    if values:
        # Формируем диапазон для обновления, начиная с A2
        range = f"'{sheet_name}'!A2"
        body = {'values': values}

        # Обновляем лист с "_creatives"
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(f"Data updated for {sheet_name} with multiple Ad Sizes and campaign info.")


def get_ad_sizes_for_campaign(service, spreadsheet_id, campaign_name):
    range = 'creatives!A:E'  # Диапазон для поиска Ad Sizes
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    values = result.get('values', [])

    ad_sizes = [row[4] for row in values if row[0] == campaign_name]
    return ad_sizes if ad_sizes else ["Unknown"]


