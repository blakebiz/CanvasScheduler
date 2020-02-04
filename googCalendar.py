from __future__ import print_function
import datetime
import pickle
import os.path
from apiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import httplib2


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def getEvents():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = get_credentials()
    # If there are no (valid) credentials available, let the user log in.


    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])



    if not events:
        return ['No upcoming events found.']
    return events

    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])


def createEvent(summary, start_time, end_time, description='', location='', timeZone='America/New_York', *args):

    credentials = get_credentials()
    service = discovery.build('calendar', 'v3', credentials=credentials)

    event = {
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_time,
        'timeZone': timeZone,
      },
      'end': {
        'dateTime': end_time,
        'timeZone': timeZone,
      },

      'reminders': {
        'useDefault': False,
        'overrides': [
          # {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    for arg in args:
        event[arg[0]] = arg[1]

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def dateFormat(date):
    string = str(date.year)[2:] + '-' + str(date.month) + '-' + str(date.day) + 'T' \
            + str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)
    return string



