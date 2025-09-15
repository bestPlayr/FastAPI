from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import Optional,Annotated, Literal
from pydantic import Field
from datetime import datetime, timezone
import json
class StudentCreate(BaseModel):
    name: str
    email: str
    age: Annotated[int, Field(gt=10,lt=100)]
    department: Optional[str] = None
    CGPA: float

class Student(StudentCreate):
        id: Annotated[UUID, Field(default_factory=uuid4)]
        created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]


def load_data():
      with open("students.json", "r") as f:
            students = json.load(f)
            return students

def save_data(students):
      with open("students.json","w") as f:
            json.dump(students,f,indent=4,default=str)



app = FastAPI()



@app.post("/create_student")
def create_student(student: StudentCreate):
      students = load_data()
      if next((s for s in students if s["email"] == student.email), None):
         raise HTTPException(status_code=400, detail="Email already exists")      
      if len(student.name.strip())<2:
            raise HTTPException(status_code=400, detail="Name must be at least 2 characters long") 
      new_student = Student(**student.dict())
      students.append(new_student.dict())
      save_data(students)
      return {"message":"Student created successfully", "student":new_student}

@app.get("/get_student/{student_id}")
def get_student(student_id: UUID):
        students = load_data()
        student = next((s for s in students if s["id"] == str(student_id)), None)
        if not student:
              raise HTTPException(status_code=404, detail="Student not found")
        return student

@app.get("/search_students")
def list_students(name: Optional[str] = None, email: Optional[str] = None, department: Optional[str] = None , sort_by_age: Optional[Literal["asc","desc"]] = None , sort_by_name: Optional[Literal["asc","desc"]] = None):
        students = load_data()
        if name:
              students = [s for s in students if name.lower() in s["name"].lower()]
              return students
        if email:
                student = next((s for s in students if s["email"] == email), None)
                return student
        if department:
              students = [s for s in students if s.get("department") and department.lower() in s["department"].lower()]
              return students
        if sort_by_age:
              if sort_by_age == "asc":
                    students.sort(key=lambda x: x["age"])
              else:
                    students.sort(key=lambda x: x["age"], reverse=True)
              return students            
        if sort_by_name:
                if sort_by_name == "asc":
                        students.sort(key=lambda x: x["name"].lower())
                else:
                        students.sort(key=lambda x: x["name"].lower(), reverse=True)
                return students
        
        return students

@app.get("/stats")
def get_stats():
        students = load_data()
        total_students = len(students)
        if total_students == 0:
              return {"No students found!"}
        average_age = sum(s["age"] for s in students)/total_students
        department_count = {}
        for s in students:
               dept = s.get("department","Not Specified")
               department_count[dept] = department_count.get(dept,0)+1
        return {"total_students": total_students, "average_age": average_age, "department_count": department_count}

@app.put("/update_student/{email}")
def update_student(student_email: str, student_update: StudentCreate):
        students = load_data()
        student = next((s for s in students if s["email"] == student_email),None)
        if not student:
              raise HTTPException(status_code=404, detail="Student not found")
        if student["email"] != student_update.email and next((s for s in students if s["email"] == student_update.email), None):
              raise HTTPException(status_code=400, detail="Email already exists")
        student.update(student_update.dict())
        save_data(students)
        return {"message":"Student updated successfully", "student":student}

@app.delete("/delete_student/{student_email}")
def delete_student(student_email: str):
        students = load_data()
        student = next((s for s in students if s["email"] == student_email), None)
        if not student:
              raise HTTPException(status_code=404, detail="Student not found")
        students.remove(student)
        save_data(students)
        return {"message":"Student deleted successfully"}



