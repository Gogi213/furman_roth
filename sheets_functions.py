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
