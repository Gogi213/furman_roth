from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def authenticate_google_services():
    # Путь к JSON-файлу учетных данных
    service_account_file = 'C:\\Users\\Redmi\\PycharmProjects\\Furman_roth\\api-for-wjat-e52acbdc91d3.json'

    # Определение областей доступа
    scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

    # Аутентификация и создание сервиса
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    drive_service = build('drive', 'v3', credentials=credentials)
    sheets_service = build('sheets', 'v4', credentials=credentials)

    return drive_service, sheets_service
