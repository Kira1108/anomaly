from sqlalchemy import (
    Boolean, 
    Column, 
    Integer, 
    String, 
    Text, 
    DateTime, 
    Float)
from sqlalchemy.sql import func

from app.database import Base

class DbOCR(Base):
    __tablename__ = 'ocr_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    ip_address = Column(Text, nullable = True)
    image_id  = Column(Integer)
    image_path = Column(Text)
    create_time = Column(DateTime, default = func.now())
    text = Column(Text)
    confidence = Column(Float)
    topleft = Column(String(50))
    topright = Column(String(50))
    bottomright = Column(String(50))
    bottomleft = Column(String(50))


class DbSex(Base):
    __tablename__ = 'sex_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    ip_address = Column(Text, nullable = True)
    image_id  = Column(Integer)
    image_path = Column(Text)
    create_time = Column(DateTime, default = func.now())
    drawings = Column(Float)
    hentai = Column(Float)
    neutral = Column(Float)
    porn = Column(Float)
    sexy = Column(Float)
    is_abnormal = Column(Boolean)


class DbText(Base):
    __tablename__ = 'text_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    ip_address = Column(Text, nullable = True)
    image_path = Column(Text, nullable = True)
    create_time = Column(DateTime, default = func.now())
    text = Column(Text)
    sensitive = Column(Boolean)
    sensitive_words = Column(Text)



class DbVideo(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    ip_address = Column(Text, nullable = True)
    create_time = Column(DateTime, default = func.now())
    video_path = Column(String(200))
    is_processed = Column(Boolean, default = False)

class DbWindow(Base):
    __tablename__ = 'windows_result'
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Text)
    image_id = Column(Integer)
    ip_address = Column(Text, nullable = True)
    image_path = Column(Text)
    create_time = Column(DateTime, default = func.now())
    confidence = Column(Float)
    is_abnormal = Column(Boolean)


class DbVideoFrames(Base):
    __tablename__ = 'video_frames'
    id = Column(Integer, primary_key=True, index=True)
    video_content_id = Column(Text)
    image_content_id = Column(Text)
    ip_address = Column(Text, nullable = True)
    image_path = Column(String(200))
    create_time = Column(DateTime, default = func.now())

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(50), nullable = True)
    password = Column(Text, nullable = False)



