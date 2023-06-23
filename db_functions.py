from datetime import date as py_date, datetime as py_datetime, time as py_time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clndr import gc_get_calendar_list
from db_classes import Base, Group, Event


def db_connect():
    engine = create_engine('sqlite:///calendar')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()

    return session


def db_set_groups(event_app):
    calendar_list = gc_get_calendar_list(event_app.gc_service)
    groups = [Group(summary=group['summary'], idGCAL=group['id']) for group in calendar_list['items']]
    for group in groups:
        if event_app.db_session.query(Group).filter(Group.idGCAL == group.idGCAL).first() is None:
            event_app.db_session.add(group)
        else:
            event_app.db_session.query(Group).filter(Group.idGCAL == group.idGCAL).update({'summary': group.summary})
    event_app.db_session.commit()

    return groups


def db_get_groups(event_app):
    return event_app.db_session.query(Group).all()


def db_set_event(idGCAL, db_session, date, start_time, end_time, title, group_idGCAL):
    if type(date) is py_datetime:
        python_date = date.date()
    else:
        print("date: ", date, "type: ", type(date))
        python_date = date
        #python_date = py_date(date.year(), date.month(), date.day())

    if type(start_time) is py_datetime:
        start_time = start_time
    else:
        start_time = py_datetime.combine(python_date, py_time(start_time.hour(), start_time.minute()))
    if type(end_time) is py_datetime:
        end_time = end_time
    else:
        end_time = py_datetime.combine(python_date, py_time(end_time.hour(), end_time.minute()))

    event = Event(idGCAL=idGCAL, date=python_date, start_time=start_time, end_time=end_time, title=title, group_idGCAL=group_idGCAL)

    if db_session.query(Event).filter(Event.idGCAL == event.idGCAL).first() is None:
        db_session.add(event)
    else:
        print("event: ", event, "type: ", type(event))
        print(event.idGCAL, event.date, event.start_time, event.end_time, event.title, group_idGCAL)
        db_session.query(Event).filter(Event.idGCAL == event.idGCAL).update({'date': event.date,
                                                            'start_time': event.start_time, 'end_time': event.end_time,
                                                            'title': event.title, 'group_idGCAL': group_idGCAL})
    db_session.commit()


def db_get_events_for_date(event_app, date):
    date = date.toString('yyyy-MM-dd')
    result = event_app.db_session.query(Event).filter(Event.date == date).all()
    result = sorted(result, key=lambda x: x.start_time)
    return result


def db_delete_event(event_app, idGCAL):
    event_app.db_session.query(Event).filter(Event.idGCAL == idGCAL).delete()
    event_app.db_session.commit()