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
    Column("course_id", ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
    Column("professor_id", ForeignKey("professors.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("course_id", "professor_id", name="course_prof_id"),
)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, nullable=False)
    rutgers_course_title = Column(String, nullable=False, unique=True)
    rutgers_course_id = Column(String, nullable=False, unique=True)
    course_credits = Column(Integer, nullable=False)
    is_elective = Column(Boolean, nullable=False, server_default="false")
    comments = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    profs = relationship(
        "Professor",
        secondary=course_professor,
        back_populates="crs",
        cascade="all, delete"
    )
    # Make a one to many from course to prof


class CourseSection(Base):
    __tablename__ = "course_sections"
    id = Column(Integer, primary_key=True, nullable=False)
    section_comments = Column(String, nullable=True)
    meeting_time = Column(String, nullable=False)
    exam_code = Column(String, nullable=False)
    section_number = Column(Integer, nullable=False)
    rutgers_course_id = Column(
        String, ForeignKey("courses.rutgers_course_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    course = relationship("Course", backref='sections')
    # unique with the combination of id and section num
    __table_args__ = (
        UniqueConstraint('rutgers_course_id', 'section_number', name='uq_rutgers_course_section'),
    )

    def __repr__(self) -> str:
        return (
            f"section_comments: {self.section_comments}\n"
            f"meeting_time: {self.meeting_time}\n"
            f"exam_code: {self.exam_code}\n"
            f"section_number: {self.section_number}\n"
            f"rutgers_course_id: {self.rutgers_course_id}\n"
        )


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
    campus = Column(String, nullable=False)
    university = Column(String, nullable=False)
    email = Column(String, nullable=False)
    classroom = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    rmp_ratings = relationship("RateMyProfessorRatings", back_populates="prof")
    crs = relationship(
        "Course",
        secondary=course_professor,
        back_populates='profs',
        cascade="all, delete"
    )
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', name='full_name'),
    )

    def __repr__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"First Name: {self.first_name}\n"
            f"Last Name: {self.last_name}\n"
            f"Campus: {self.campus}\n"
            f"Uni: {self.university}\n"
            f"Email: {self.email}\n"
            f"Created At: {self.created_at}\n"
        )
    # have a back populates relationship


class RateMyProfessorRatings(Base):
    __tablename__ = "rmp_ratings"
    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(String, nullable=False)
    student_reviews = Column(String, nullable=False)
    prof_quality = Column(Integer, nullable=False)
    prof_difficulty = Column(Integer, nullable=False)
    rutgers_course_title = Column(String, nullable=False)
    student_experience = Column(String, nullable=False)
    grade_received = Column(String, nullable=True, server_default=None)
    textbook = Column(Boolean, nullable=True, server_default=None)
    would_take_again = Column(Boolean, nullable=True, server_default=None)
    attendance = Column(Boolean, nullable=True, server_default=None)
    # prof = relationship("Professor", back_populates="prof")
    prof_id = Column(Integer, ForeignKey('professors.id'), nullable=False)
    prof = relationship("Professor", back_populates="rmp_ratings")
