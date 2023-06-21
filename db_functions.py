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


def db_load_groups(event_app):
    calendar_list = gc_get_calendar_list(event_app.gc_service)
    groups = [Group(summary=group['summary'], idGCAL=group['id']) for group in calendar_list['items']]
    for group in groups:
        if event_app.db_session.query(Group).filter(Group.idGCAL == group.idGCAL).first() is None:
            event_app.db_session.add(group)
    event_app.db_session.commit()

    event_app.group_titles = [group.summary for group in groups]


def db_get_groups(event_app):
    return event_app.db_session.query(Group).all()


def db_load_event(idGCAL, db_session, date, start_time, end_time, title, group):
    python_date = py_date(date.year(), date.month(), date.day())
    start_datetime = py_datetime.combine(python_date, py_time(start_time.hour(), start_time.minute()))
    end_datetime = py_datetime.combine(python_date, py_time(end_time.hour(), end_time.minute()))
    group = db_session.query(Group).filter(Group.summary == group).first()
    group_idGCAL = group.idGCAL
    event = Event(idGCAL=idGCAL, date=python_date, start_time=start_datetime, end_time=end_datetime, title=title, group=group_idGCAL)

    if db_session.query(Event).filter(Event.idGCAL == event.idGCAL).first() is None:
        db_session.add(event)
    db_session.commit()


def db_get_events_for_date(event_app, date):
    date = date.toString('yyyy-MM-dd')
    result = event_app.db_session.query(Event).filter(Event.date == date).all()
    result = sorted(result, key=lambda x: x.start_time)
    return result


def db_delete_event(event_app, idGCAL):
    event_app.db_session.query(Event).filter(Event.idGCAL == idGCAL).delete()
    event_app.db_session.commit()