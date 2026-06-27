from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Automatically database tables create karna agar pehle se nahi bani hain
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Jinja2 Templates folder ka setup
import os
# Purani line ko hata kar ye likhein:
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))


# ----------------------------------------------------
# 1. FRONTEND ROUTE (Home Page)
# ----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    # Database se saare students lekar HTML page par render karna
    students = db.query(models.Student).all()
    return templates.TemplateResponse("index.html", {"request": request, "students": students})


# ----------------------------------------------------
# 2. API ENDPOINTS (CRUD OPERATIONS)
# ----------------------------------------------------

# [CREATE] - Naya student add karne ke liye
@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentBase, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name, age=student.age, course=student.course)
    db.add(db_student)
    db.commit()
    db.refresh(db_student) # ID generate hone ke baad data refresh karega
    return db_student


# [READ] - Saare students ki list dekhne ke liye (JSON Format)
@app.get("/students", response_model=list[schemas.StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


# [UPDATE] - Kisi student ki details badalne ke liye
@app.put("/students/{id}", response_model=schemas.StudentResponse)
def update_student(id: int, updated_student: schemas.StudentBase, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Nayi values set karna
    db_student.name = updated_student.name
    db_student.age = updated_student.age
    db_student.course = updated_student.course
    
    db.commit()
    db.refresh(db_student)
    return db_student


# [DELETE] - Kisi student ko database se hatane ke liye
@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()
    return {"message": f"Student with ID {id} has been deleted successfully."}