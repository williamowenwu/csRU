from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    text,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
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
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    profs = relationship("Professor", secondary=course_professor, back_populates="crs")
    # Make a one to many from course to prof


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    id = Column(Integer, primary_key=True, nullable=False)


class Professor(Base):
    __tablename__ = "professors"
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    crs = relationship("Course", secondary=course_professor, back_populates="profs")

    # have a back populates relationship
