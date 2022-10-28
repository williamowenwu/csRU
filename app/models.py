from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from .database import Base

class Course(Base):
    __tablename__ = 'courses'    
    id  = Column(Integer, primary_key=True, nullable=False)
    course_title = Column(String,nullable=False)
    rutgers_course_id = Column(String,nullable=False)
    is_elective = Column(Boolean,nullable=False, server_default='false')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    id  = Column(Integer, primary_key=True, nullable=False)

class Professor(Base):
    __tablename__ = "professors"
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, 
                        server_default=text('now()'))

class Prof_Course(Base):
    __tablename__ = "professors_courses"
    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, 
                       ForeignKey("courses.id", ondelete="CASCADE"), 
                       nullable=False)
    professor_id = Column(Integer, 
                          ForeignKey("professors.id", ondelete="CASCADE"),
                          nullable=False)
    course_name = relationship(Course)
    prof_name = relationship(Professor)