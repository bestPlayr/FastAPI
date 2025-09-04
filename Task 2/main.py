from fastapi import FastAPI,HTTPException, Path, Query
import json
app = FastAPI()

data = []

with open('students.json','r') as file:
    data = json.load(file)

@app.get("/students")
def get_students():
   if not data:
       raise HTTPException(status_code=404, detail="No data found")
   return data  

@app.get("/student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve")):
    if not data:
        raise HTTPException(status_code=404,detail="No data found")
    student = next((student for student in data if student["id"] == student_id), None)
    if student:
        return student
    raise HTTPException(status_code=404,detail="Student not found")

@app.get("/sort_students")
def sort_students(sort_by:str = Query('desc', description="Sort order: 'asc' or 'desc'")):
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    if sort_by not in ['asc','desc']:
        raise HTTPException(status_code=400, detail = "Invalid sort order. Must be either 'asc' or 'desc'")
    reverse = True if sort_by == 'desc' else False 
    sorted_students = sorted(data , key=lambda x: x['CGPA'], reverse=reverse)   
    return sorted_students




