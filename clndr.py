import os.path
import datetime as dt
import time

from PySide6.QtWidgets import QMessageBox
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib3 import HTTPSConnectionPool

SCOPES = ['https://www.googleapis.com/auth/calendar']


def auth():
    try:
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
    #no internet connection:
    except HTTPSConnectionPool:
        msg = QMessageBox()
        msg.setWindowTitle("No internet connection")
        msg.setText("You are not connected to the internet. Please connect and try again.")
        msg.setIcon(QMessageBox.Critical)
        msg.exec()
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
    events = []

    for calendar in calendar_list['items']:
        events_result = service.events().list(calendarId=calendar['id'], timeMin=now,
                                              singleEvents=True, orderBy='startTime').execute()

        sorted_events = sorted(events_result.get("items", []),
                               key=lambda x: x.get("start", {}).get("dateTime", x.get("start", {}).get("date", "")))

        for sorted_event in sorted_events:
            imported_event = {
                'id': sorted_event['id'],
                'date': dt.datetime.strptime(sorted_event['start']['dateTime'][:10], '%Y-%m-%d'),
                'start_time': dt.datetime.strptime(sorted_event['start']['dateTime'][11:16], '%H:%M'),
                'end_time': dt.datetime.strptime(sorted_event['end']['dateTime'][11:16], '%H:%M'),
                'title': sorted_event['summary'],
                'group': calendar['id']
            }
            print(calendar['id'], calendar['summary'], sorted_event['summary'])
            events.append(imported_event)

    return events


# construct event object, based input date, time, title and calendar id
def gc_create_event(date, start_time, end_time, title):
    if type(date) is dt.date:
        date = date.strftime('%Y-%m-%d')
    else:
        date = date.toString('yyyy-MM-dd')
    # date = date.toString('yyyy-MM-dd')
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
def gc_upload_event(service, event, old_group, new_group):
    old_calendar_id = None
    new_calendar_id = None
    for item in gc_get_calendar_list(service)['items']:
        if item['id'] == old_group:
            old_calendar_id = item['id']
            break

    for item in gc_get_calendar_list(service)['items']:
        if item['id'] == new_group:
            new_calendar_id = item['id']
            break

    # if event exists, update it, else create new
    if event['id'] is not None:
        try:
            if service.events().get(calendarId=old_calendar_id, eventId=event['id']).execute():
                if old_calendar_id == new_calendar_id:
                    event = service.events().update(calendarId=old_calendar_id, eventId=event['id'], body=event).execute()
                    return event['id']
                else:

                        service.events().delete(calendarId=old_calendar_id, eventId=event['id']).execute()
        #ignore error 410
        except HttpError as err:
            if err.resp.status == 404:
                service.events().delete(calendarId=old_calendar_id, eventId=event['id']).execute()
            else:
                pass

    #wait for 1 sec to avoid error 409
    time.sleep(1)
    #avoiding error 410
    event['id'] = None
    event = service.events().insert(calendarId=new_calendar_id, body=event).execute()
    return event['id']


# delete event from calendar
def gc_delete_event(app, event):
    try:
        service = app.gc_service
        #find event.group.currentText() == 'summary'
        calendars = gc_get_calendar_list(service)['items']
        for item in calendars:
            if item['summary'] == event.group.currentText():
                calendar_id = item['id']
                break
        service.events().list(calendarId=calendar_id).execute()
        if calendar_id is not None and event.idGCAL is not None:
            service.events().delete(calendarId=calendar_id, eventId=event.idGCAL).execute()
        else:
            alert = QMessageBox()
            alert.setText("Event not found!")

    except HttpError as err:
        print("An error occured: ", err)
