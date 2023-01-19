from __future__ import print_function

import os.path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Documentação online
# https://developers.google.com/sheets/api/reference/rest?hl=pt-br

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Credenciais de API
def my_creds():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes=SCOPES)
    
    if not creds or creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES)
            
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def nova_planilha(sheet_name):
    """
    spreadsheet = {
        'properties': {'title': sheet_name}
    }
    """

    creds = my_creds()

    spreadsheet = {
        'properties': {'title': sheet_name}
    }

    try:

        service = build('sheets','v4',credentials=creds)

        request = service.spreadsheets().create(body=spreadsheet,fields='spreadsheetId')

        response = request.execute()

        print(response)
        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
