from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# 스코프 설정 및 credentials.json 파일 로드
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

# 이미 생성된 토큰 파일이 있는 경우 로드
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# 토큰이 없거나 유효하지 않은 경우, 사용자 인증을 위해 새로운 토큰 생성
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('tomatalerdriveaccess.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Google Drive API 클라이언트 생성
service = build('drive', 'v3', credentials=creds)

# 파일 목록 가져오기
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

# 여기서 특정 파일 ID를 사용하여 파일을 다운로드하거나 처리할 수 있습니다.
