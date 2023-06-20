from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///calendar.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    summary = Column(String)
    # color = Column(String)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    odGCAL = Column(String, unique=True)
    title = Column(String)
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    group = Column(String)


# add tables to database
def create_tables():
    Base.metadata.create_all(engine)


def add_group(id, summary):
    new_group = Group(summary=summary, id=id)
    session.add(new_group)
    session.commit()

def get_groups():
    return session.query(Group).all()

def get_events_by_date(date):
    return session.query(Event).filter_by(date=date).all()

def write_data_to_db(data):
    for row in data:
        session.add(row)
    session.commit()
