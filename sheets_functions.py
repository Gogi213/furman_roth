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


def update_creative_sheets_with_dates(service, spreadsheet_id, sheet_name, data):
    dates = get_dates_for_current_month()

    # Предполагаем, что data содержит данные, которые нужно распределить по дням
    # Равномерное распределение данных по дням (простой пример, можно адаптировать)
    distributed_data = [data for _ in dates]

    # Формируем значения для обновления
    values = []
    for date, data in zip(dates, distributed_data):
        row = [date] + data  # Добавляем дату в начало каждой строки данных
        values.append(row)

    # Диапазон для обновления, A2 стартует с 2-й строки, так как 1-я для заголовков
    range = f'{sheet_name}!A2'
    body = {'values': values}

    # Обновляем лист с "_creatives"
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    print(f"{result.get('updatedCells')} cells updated.")


def update_creative_sheets_with_dates(service, spreadsheet_id, sheet_name, fact_data, ad_size):
    dates = get_dates_for_current_month()

    for row in fact_data:
        # Извлекаем имя кампании и другие данные из строки fact
        campaign_name, advertiser, campaign, tactic, impressions, clicks = row[:6]
        ad_size = get_ad_size_for_campaign(service, spreadsheet_id, campaign_name)

        values = []
        for date in dates:
            # Формируем строку с добавлением даты и Ad Size
            values.append([campaign_name, advertiser, campaign, tactic, date, ad_size, impressions, clicks])

        sheet_name = f"{campaign_name}_creatives"  # Формат имени листа
        range = f"'{sheet_name}'!A2"  # Диапазон обновления, начиная со второй строки

        body = {'values': values}
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(f"Data updated for {sheet_name}.")


def get_ad_size_for_campaign(service, spreadsheet_id, campaign_name):
    range = 'creatives!A:E'  # Предположим, что столбец E содержит Ad Size
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    values = result.get('values', [])

    for row in values:
        if row[0] == campaign_name:  # Проверяем, соответствует ли значение в столбце A имени кампании
            return row[4]  # Возвращаем значение из столбца E (Ad Size)
    return "Unknown"  # Возвращаем "Unknown", если соответствие не найдено

