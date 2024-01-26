from sqlalchemy.orm import Session

import models
import schemas

def create_quiz(db: Session, quiz:schemas.QuizCreate):
    db_quiz = models.Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def get_quizzes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quiz).offset(skip).limit(limit).all()

def create_teacher(db: Session, teacher:schemas.TeacherCreate):
    db_teacher = models.Teacher(name=teacher.name, course=teacher.course, quiz_id=teacher.quiz_id)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def get_quiz_questions(db: Session, quiz_id: int):
    return db.query(models.Questions).filter(models.Questions.quiz_id == quiz_id).all()

def create_quiz_questions(db: Session, quiz_question: schemas.QuestionCreate):
    db_quiz_question = models.Questions(**quiz_question.dict())
    db.add(db_quiz_question)
    db.commit()
    db.refresh(db_quiz_question)
    return db_quiz_question

def delete_quiz_questions(db: Session, quiz_id: int, quiz_questions_id: int):
    db_quiz_question = db.query(models.Questions).filter(models.Questions.id == quiz_questions_id, models.Questions.quiz_id == quiz_id).first()
    if db_quiz_question:
        db.delete(db_quiz_question)
        db.commit()
        return db_quiz_question
    return None

def create_answer(db: Session, question_answer: schemas.AnswersCreate):
    db_question_answer = models.Answers(r_number=question_answer.r_number, answer=question_answer.answer, question_id=question_answer.question_id, quiz_id=question_answer.quiz_id)
    db.add(db_question_answer)
    db.commit()
    db.refresh(db_question_answer)
    return db_question_answer
