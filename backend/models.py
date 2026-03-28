from sqlalchemy import Column, Integer, String, Text,Float
from db import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    skills = Column(Text)
    education = Column(Text)
    experience = Column(Text)
    raw_text = Column(Text)

    score = Column(Float,default=0.0)


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(255))
    content = Column(Text)


