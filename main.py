from auth import authenticate_google_services
from sheets_functions import (
    get_unique_values,
    create_creative_reports_sheets,
    get_fact_data,
    update_creative_sheets_with_dates,
    get_ad_sizes_for_campaign  # Убедитесь, что эта функция существует и импортирована
)

def main():
    # Аутентификация и получение доступа к сервисам Google Sheets
    drive_service, sheets_service = authenticate_google_services()

    # ID Google Spreadsheet
    spreadsheet_id = '1BTAu2VY_0ysyc7SkjnPoWtiYZ9gLLBWf3ixhx8fn_58'

    # Получаем уникальные значения для создания листов "_creatives"
    unique_values = get_unique_values(sheets_service, spreadsheet_id, 'fact!A:A')

    # Создаем листы "_creatives", если они еще не созданы
    create_creative_reports_sheets(sheets_service, spreadsheet_id, unique_values)

    # Получаем данные из листа "fact"
    fact_data = get_fact_data(sheets_service, spreadsheet_id)

    # Получаем данные для каждой уникальной кампании и обновляем соответствующие листы
    for campaign_name in unique_values:
        formatted_sheet_name = f"{campaign_name}_creatives"
        # Теперь функция update_creative_sheets_with_dates принимает только 4 аргумента
        update_creative_sheets_with_dates(sheets_service, spreadsheet_id, formatted_sheet_name, fact_data)


if __name__ == '__main__':
    main()
