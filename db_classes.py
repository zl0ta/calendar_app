from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idGCAL = Column(String, unique=True)
    summary = Column(String, unique=True)


class Event(Base):
    __tablename__ = 'events'
    idGCAL = Column(String, primary_key=True)
    title = Column(String)
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    group = Column(String)