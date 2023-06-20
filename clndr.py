import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def auth():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# get service object
def get_service():
    try:
        creds = auth()
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as err:
        print("An error occured: ", err)

# get list of all calendars
def get_calendar_list(service):
    calendar_list = service.calendarList().list().execute()
    return calendar_list

# get list of all events from all calendars
def get_events(service):
    now = dt.datetime.now().isoformat() + 'Z'
    calendar_list = get_calendar_list(service)

    # add all events from all calendars to events_result
    events_result = []
    for item in calendar_list['items']:
        events_result.append(service.events().list(calendarId=item['id'], timeMin=now,
                                                   singleEvents=True, orderBy='startTime').execute())

    events = []
    for result in events_result:
        events.extend(result.get("items", []))
        events = sorted(events, key=lambda x: x["start"].get("dateTime", x["start"].get("date")))

    if not events:
        print("No upcoming events found!")
        return

    '''
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
    '''

    return events

# construct event object, based input date, time, title and calendar id
def create_event(date, start_time, end_time, title, group):
    event = {
        'summary': title,
        'location': group,
        'description': 'Event created by Events Calendar App',
        'start': {
            'dateTime': date + 'T' + start_time + ':00',
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': date + 'T' + end_time + ':00',
            'timeZone': 'Europe/Moscow',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    return event

# upload event to calendar
def upload_event(service, event):
    try:
        service.events().insert(calendarId=event['cal_id'], body=event).execute()
        print("Event created successfully!")
    except HttpError as err:
        print("An error occured: ", err)
