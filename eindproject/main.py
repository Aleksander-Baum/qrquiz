import os

from fastapi import FastAPI, Depends, HTTPException, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pyzbar.pyzbar import decode
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

import models
import schemas
import crud
from database import SessionLocal, engine

if not os.path.exists('.\mysqldb'):
    os.makedirs('.\mysqldb')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


qr_code_dict = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/", response_class=HTMLResponse)
def read_root():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "start_scan":
            # Call your QR code scanning logic here
            # For example: read_qr_code(frame)
            # Process the data and emit the result using websocket.send_text(result)
            await websocket.send_text(jsonable_encoder({"message": "Scanning started."}))
        elif data == "stop_scan":
            # Stop QR code scanning logic
            # For example: stop_scan()
            # Optionally, you can send a message indicating that scanning has stopped
            await websocket.send_text(jsonable_encoder({"message": "Scanning stopped."}))

@app.post("/quiz/", response_model=schemas.Quiz)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    return crud.create_quiz(db=db, quiz=quiz)

@app.get("/quizzes/", response_model=list[schemas.Quiz])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quizzes = crud.get_quizzes(db, skip, limit)
    return quizzes

@app.get("/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@app.post("/teacher/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db=db, teacher=teacher)

@app.get("/teachers/", response_model=list[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db, skip, limit)
    return teachers

@app.post("/question/", response_model=schemas.Question)
def create_quiz_question(quiz_question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_quiz_questions(db=db, quiz_question=quiz_question)

@app.get("/questions/{quiz_id}", response_model=list[schemas.Question])
def read_quiz_questions(quiz_id: int, db: Session = Depends(get_db)):
    quiz_questions = crud.get_quiz_questions(db, quiz_id)

    if not quiz_questions:
        raise HTTPException(status_code=404, detail="Quiz not found or no questions in quiz")

    return quiz_questions

@app.delete("/quizzes/{quiz_id}/quizquestions/{quiz_question_id}", response_model=schemas.Question)
def delete_quiz_question(quiz_id: int, quiz_question_id: int, db: Session = Depends(get_db)):
    deleted_quiz_question = crud.delete_quiz_questions(db, quiz_id, quiz_question_id)

    if deleted_quiz_question is None:
        raise HTTPException(status_code=404, detail="Quiz or question not found")

    return deleted_quiz_question

@app.post("/answer/")
def create_quiz_question_answers(question_answer: schemas.AnswersCreate, db: Session = Depends(get_db)):
    return crud.create_answer(db=db, question_answer=question_answer)

# Function to read QR code from a frame
def read_qr_code(frame):
    decoded_objects = decode(frame)

    if decoded_objects:
        qr_code = decoded_objects[0]
        orientation = qr_code.orientation
        data = qr_code.data.decode('utf-8')

        if orientation == 'UP':
            letter_orientation = 'A'
        elif orientation == 'RIGHT':
            letter_orientation = 'B'
        elif orientation == 'DOWN':
            letter_orientation = 'C'
        elif orientation == 'LEFT':
            letter_orientation = 'D'
        else:
            letter_orientation = orientation

        return {"orientation": letter_orientation, "data": data}
    else:
        return None
