import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from apiclient import errors
import dateutil.parser
from datetime import datetime
import pytz

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def delete_old_backup():
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
            if item['name'] == 'hockey_db_backup.sql':
                print(dateutil.parser.isoparse(item['modifiedTime']))
                if dateutil.parser.isoparse(item['modifiedTime']) < minTime:
                    minTime = dateutil.parser.isoparse(item['modifiedTime'])
                    oldBackupID = item['id']
    try:
        service.files().delete(fileId=oldBackupID).execute()
    except errors.HttpError:
        print('Error Occured')


def get_new_backup_usb():
    os.system("mysqldump -u root -proot -h 'localhost' hockey > /media/pi/ESD-USB/hockey.sql")
    os.system("mysqldump -u root -proot -h 'localhost' draft_kings > /media/pi/ESD-USB/draft_kings.sql")
    os.system("mysqldump -u root -proot -h 'localhost' stage_hockey > /media/pi/ESD-USB/stage_hockey.sql")

def get_new_backup_ssd():
    os.system("mysqldump -u root -proot -h 'localhost' hockey > /home/pi/Documents/mysql_backups/hockey.sql")
    os.system("mysqldump -u root -proot -h 'localhost' draft_kings > /home/pi/Documents/mysql_backups/draft_kings.sql")
    os.system("mysqldump -u root -proot -h 'localhost' stage_hockey > /home/pi/Documents/mysql_backups/stage_hockey.sql")


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

    file_metadata = {'name': 'hockey_db_backup.sql', 'parents': [folderID]}

    media = MediaFileUpload(filename='/home/pi/Documents/mysql_backups/hockey_db_backup.sql', resumable=True)

    # service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    request = service.files().create(body=file_metadata, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded: {int(status.progress() * 100)}%")

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
