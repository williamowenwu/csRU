from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.storage.database import Base

course_professor = Table(
    "course_professor",
    Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("professor_id", ForeignKey("professors.id"), primary_key=True),
    UniqueConstraint("course_id", "professor_id", name="course_prof_id"),
)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, nullable=False)
    course_title = Column(String, nullable=False, unique=True)
    rutgers_course_id = Column(String, nullable=False, unique=True)
    is_elective = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    profs = relationship("Professor", secondary=course_professor, back_populates="crs")
    # Make a one to many from course to prof


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    university = Column(String, nullable=False)
    email = Column(String, nullable=False)
    classroom = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    crs = relationship("Course", secondary=course_professor, back_populates="profs")

    # have a back populates relationship
