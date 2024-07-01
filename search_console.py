from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Замінити на шлях до вашого JSON-файлу ключа
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/your/key.json'

def main():
    # Авторизація за допомогою JSON-файлу ключа
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    service = build('webmasters', 'v3', credentials=credentials)

    # Замінити на URL-адресу вашого сайту
    site_url = 'https://example.com'

    # Отримати дані про сайт
    site_data = service.sites().get(siteUrl=site_url).execute()

    # Вивести дані сайту
    print(f"Назва сайту: {site_data['name']}")
    print(f"URL сайту: {site_data['url']}")
    print(f"Власник сайту: {site_data['ownershipType']}")

if __name__ == '__main__':
    main()
    