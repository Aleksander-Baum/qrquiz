from typing import List
from pydantic import BaseModel

class QuizBase(BaseModel):
    name: str

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int

    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    name: str
    course: str
    quiz_id: int

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    question_title: str
    answer_a: str
    answer_b: str
    answer_c: str
    answer_d: str
    correct_answer: str
    quiz_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class AnswersBase(BaseModel):
    r_number: str
    answer: str
    question_id: int
    quiz_id: int

class AnswersCreate(AnswersBase):
    pass

class Answers(AnswersBase):
    id: int

    class Config:
        orm_mode = True

class QuestionWithAnswers(QuestionBase):
    answers: List[Answers] = []

    class Config:
        orm_mode = True