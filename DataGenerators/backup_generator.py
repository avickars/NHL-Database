from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def upload_backup():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    folderID = '1C-sjhFggAlxcjkVf529o8iP7JA87znYh'

    # file_metadata = {'name':'test.csv', 'parents':[folderID]}

    file_metadata = {'name': '~/Documents/mysql_backups/hockey_db_backup.sql', 'parents': [folderID]}

    media = MediaFileUpload(filename='hockey_db_backup.sql')
    # media = MediaFileUpload(filename='test.csv', mimetype='text/csv')

    service.files().create(body = file_metadata, media_body = media, fields='id').execute()

    # # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])
    #
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))





