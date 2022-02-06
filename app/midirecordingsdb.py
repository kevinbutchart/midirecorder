from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time
from pprint import pprint
from collections import OrderedDict
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()


class RecordingData(Base):
    __tablename__ = 'recording_data'
    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary)
 
class RecordingList(Base):
    __tablename__ = 'recording_list'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    datetime = Column(DateTime)
    duration = Column(Float)
    title = Column(String(250))
    section = Column(String(250))
    score = Column(Integer)
    comment = Column(String)
    favourite = Column(Boolean)
    data_id = Column(Integer, ForeignKey('recording_data.id'))
    data = relationship(RecordingData)


class MidiRecordingsDB:
    def __init__(self, db_url):
        engine = create_engine(
            db_url, connect_args={"check_same_thread": False}
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(engine)
        #Base.metadata.bind = engine
     
        self.session = SessionLocal()
        self.last_fetched_id = -1 

    def get_recording(self, id):
        return self.session.query(RecordingList).get(id)

    def add_recording(self, data, duration):
        new_midifile = RecordingData(data=data)
        self.session.add(new_midifile)
        self.session.commit()

        date_time_obj = datetime.utcnow()
        title = '' 
        name = date_time_obj.strftime("%Y_%m%d_%H%M%S.mid")
        duration = duration 
        favourite = False 

        new_recording = RecordingList(title= title, name=name, datetime=date_time_obj, duration=duration, favourite=favourite, data=new_midifile)
        self.session.add(new_recording)
        self.session.commit()
        return new_recording.id

    def get_recent_recordings(self, limit):
        return self.session.query(RecordingList).order_by(RecordingList.datetime.desc()).limit(limit)

    def get_new_recordings(self):
        if self.last_fetched_id == -1:
            return []
        q = self.session.query(RecordingList).order_by(RecordingList.datetime.desc()).filter(RecordingList.id > self.last_fetched_id).limit(15)
        count = q.count()
        if count > 0:
            self.last_fetched_id = q.first().id 
        return list(q)

    def get_recordings_by_date(self, limit=None, title_filter=None):
        recordings_dict = OrderedDict() 
        last_id = 0
        query = self.session.query(RecordingList.id,
                                    RecordingList.datetime,
                                    RecordingList.duration,
                                    RecordingList.name,
                                    RecordingList.title,
                                    RecordingList.favourite).order_by(RecordingList.datetime.desc())
        if limit is not None:
            query = query.limit(limit)
        if title_filter is not None:
            query = query.filter(RecordingList.title.contains(title_filter))

        for instance in query:
            if instance.id > last_id:
                last_id = instance.id
            day_recordings = recordings_dict.get(instance.datetime.date(), [])
            day_recordings.append( instance ) 
            recordings_dict[instance.datetime.date()] = day_recordings
        self.last_fetched_id = last_id
        return recordings_dict

    def get_titles(self):
        titles = list() 
        last_id = 0
        for instance in self.session.query(RecordingList.title).distinct():
            titles.append(instance.title)
        return titles 

    def commit(self):
        self.session.commit()

if __name__ == '__main__':
    db = MidiRecordingsDB()
    recs = db.get_recordings_by_date(250)
    pprint(recs)
