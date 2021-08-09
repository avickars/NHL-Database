import pandas as pd
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from apiclient import errors
import pytz
import dateutil.parser
from datetime import datetime
import httplib2
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def delete_old_backup(file):
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

    # folderID = '1C-sjhFggAlxcjkVf529o8iP7JA87znYh'

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, modifiedTime)").execute()
    items = results.get('files', [])

    oldBackupID = 'NULL'
    utc = pytz.UTC
    minTime = utc.localize(datetime(2030, 11, 28, 23, 55, 59, 342380))
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            if item['name'] == file:
                if dateutil.parser.isoparse(item['modifiedTime']) < minTime:
                    minTime = dateutil.parser.isoparse(item['modifiedTime'])
                    oldBackupID = item['id']
    try:
        service.files().delete(fileId=oldBackupID).execute()
    except errors.HttpError:
        print('Error Occured')


def upload_data(path,file):
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

    folderID = '1_ZUd7dxIzwsT26ORlGc6sYcSEwGIYJxI'

    file_metadata = {'name': file, 'parents': [folderID]}

    media = MediaFileUpload(filename=path+file, resumable=True)

    # service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    request = service.files().create(body=file_metadata, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded: {int(status.progress() * 100)}%")






def main():
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, 'production_hockey', creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    tables = ['conferences_view',
              'daily_update_script_execution',
              'divisions_view',
              'game_sheet_skaters_view',
              'goalies_boxscores',
              'player_information_view',
              'schedules',
              'teams_view',
              'trophy_winners_view',
              'weekly_update_script_execution']

    for table in tables:
        print(table)
        data = pd.read_sql_query(sql=f"select * from {table}", con=connection)
        data.to_csv(f"PowerBI Tables/{table}.csv")
        # delete_old_backup(f"{table}.xlsx")
        upload_data('PowerBI Tables/', f"{table}.csv")




if __name__ == '__main__':
    main()



