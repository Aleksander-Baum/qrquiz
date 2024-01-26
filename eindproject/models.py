from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from database import Base


class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)

class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    course = Column(String(75), index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))

class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_title = Column(String(255), index=True)
    answer_a = Column(String(255), index=True)
    answer_b = Column(String(255), index=True)
    answer_c = Column(String(255), index=True)
    answer_d = Column(String(255), index=True)
    correct_answer = Column(Enum('A', 'B', 'C', 'D'), index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))

class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    r_number = Column(String(20), index=True)
    answer = Column(String(5), index=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

