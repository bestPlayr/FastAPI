from fastapi import FastAPI,HTTPException, Path
from pydantic import BaseModel, Field, field_validator
from typing import Annotated,Optional
import json


class Student(BaseModel):
    id: Annotated[int,Field(gt=0,description="Student's unique ID",examples=[1,2,3])]
    name: Annotated[str,Field(min_length=2,max_length=50,description="Student's full name")]
    age: Annotated[int,Field(gt=5,lt=100,description="Student's age")]
    roll_number: Annotated[str,Field(description="Student's roll number",examples=["R001","R002"])]
    grade: Optional[Annotated[str,Field(description="Student's grade",examples=['A','B','C'])]] = None
    
    @field_validator('id')
    @classmethod
    def id_validator(cls,id):
        if data and any(student['id'] == id for student in data):
            raise ValueError("ID must be unique")
        return id

    @field_validator('name')
    @classmethod
    def name_validator(cls,name):
        if not name.strip():
            raise ValueError("Enter a valid name")      
        return name
    
    @field_validator('roll_number')
    @classmethod
    def roll_number_validator(cls,roll_number):
        if data and any(student['roll_number'] == roll_number for student in data):
            raise ValueError("Roll number must be unique")
        return roll_number

data = []
with open('students.json','r') as file:
    data = json.load(file)    

app = FastAPI()

@app.get("/students")
def get_students():
   if not data:
       raise HTTPException(status_code=404, detail="No data found")
   return data  

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve")):
    if not data:
        raise HTTPException(status_code=404,detail="No data found")
    student = next((student for student in data if student["id"] == student_id), None)
    if student:
        return student
    raise HTTPException(status_code=404,detail="Student not found")


@app.post("/students")
def add_student(student: Student):
       try:
           data.append(student.model_dump())
           with open('students.json','w') as f:
               f.write(json.dumps(data,indent=4))
           return {"message":"Student added successfully"}
    
       except Exception as e:
           raise HTTPException(status_code=500,detail="Failed to add student")         
