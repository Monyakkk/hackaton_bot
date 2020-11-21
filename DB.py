from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()
engine = create_engine("sqlite:///Database.db")
session = sessionmaker(bind=engine)

class Timetable(Base):
    __tablename__ = 'timetable'
    GroupID = Column(String)
    Time = Column(String)
    Subject = Column(String)
    ZoomLink = Column(String)


    __table_args__ = (
         PrimaryKeyConstraint(
            GroupID,
            Time),
         {})


class Groups(Base):
    __tablename__ = 'Groups'
    GroupID = Column(String)
    TelegramID = Column(String, primary_key= True)


Base.metadata.create_all(engine)
