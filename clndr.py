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
def gc_get_service():
    try:
        creds = auth()
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as err:
        print("An error occured: ", err)


# get list of all calendars
def gc_get_calendar_list(service):
    calendar_list = service.calendarList().list().execute()
    return calendar_list


# get list of all events from all calendars
def gc_get_events(service):
    now = dt.datetime.now().isoformat() + 'Z'
    calendar_list = gc_get_calendar_list(service)

    # add all events from all calendars to events_result
    events_result = []
    for item in calendar_list['items']:
        events_result.append(service.events().list(calendarId=item['id'], timeMin=now,
                                                   singleEvents=True, orderBy='startTime').execute())

    events_items = []
    for result in events_result:
        events_items.extend(result.get("items", []))
        events_items = sorted(events_items, key=lambda x: x["start"].get("dateTime", x["start"].get("date")))

    if not events_items:
        print("No upcoming events found!")
        return

    # Format: event = {idGCAL, title, date, start_time, end_time, calendar_summary}
    events = []
    for item in events_items:
        event = {
            'id': item['id'],
            'title': item['summary'],
            # get date, start_time and end_time from '2023-06-21T15:15:00+02:00' format string
            'date': dt.datetime.strptime(item['start']['dateTime'][:10], '%Y-%m-%d'),
            'start_time': dt.datetime.strptime(item['start']['dateTime'][11:16], '%H:%M'),
            'end_time': dt.datetime.strptime(item['end']['dateTime'][11:16], '%H:%M'),
            'calendar': item
        }
        events.append(event)

    return events


# construct event object, based input date, time, title and calendar id
def gc_create_event(date, start_time, end_time, title):
    date = date.toString('yyyy-MM-dd')
    start_time = start_time.toString('HH:mm')
    end_time = end_time.toString('HH:mm')
    event = {
        'summary': title,
        'description': 'Event created by Events Calendar App',
        'location': 'Wroclaw, Poland',
        'start': {
            # 'dateTime': '2021-05-20T09:00:00',
            'dateTime': date + 'T' + start_time + ':00',
            'timeZone': 'Europe/Warsaw',
        },
        'end': {
            'dateTime': date + 'T' + end_time + ':00',
            'timeZone': 'Europe/Warsaw',
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
def gc_upload_event(service, event, group):
    for item in gc_get_calendar_list(service)['items']:
        if item['summary'] == group:
            calendar_id = item['id']
            break
    event = service.events().insert(calendarId=calendar_id, body=event).execute()

    return event['id']


# delete event from calendar
def gc_delete_event(app, event):
    try:
        service = app.gc_service
        calendar_id = None
        for item in gc_get_calendar_list(service)['items']:
            if item['summary'] == event.group_data:
                calendar_id = item['id']
                break
        print(event.idGCAL)
        service.events().list(calendarId=calendar_id).execute()
        service.events().delete(calendarId=calendar_id, eventId=event.idGCAL).execute()
    except HttpError as err:
        print("An error occured: ", err)
