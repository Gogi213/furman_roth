from auth import authenticate_google_services
from sheets_functions import get_unique_values, create_creative_reports_sheets

def main():
    drive_service, sheets_service = authenticate_google_services()

    # ID Google Spreadsheet
    spreadsheet_id = '1BTAu2VY_0ysyc7SkjnPoWtiYZ9gLLBWf3ixhx8fn_58'
    range = 'fact!A:A'  # Диапазон для получения уникальных значений

    unique_values = get_unique_values(sheets_service, spreadsheet_id, range)
    create_creative_reports_sheets(sheets_service, spreadsheet_id, unique_values)

if __name__ == '__main__':
    main()
