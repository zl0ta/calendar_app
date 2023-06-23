from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    idGCAL = Column(String, primary_key=True)
    summary = Column(String)

    events = relationship('Event', back_populates='group')

class Event(Base):
    __tablename__ = 'events'
    idGCAL = Column(String, primary_key=True)
    title = Column(String)
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    group_idGCAL = Column(String, ForeignKey('groups.idGCAL'))

    group = relationship('Group', back_populates='events')