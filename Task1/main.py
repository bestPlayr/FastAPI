from fastapi import FastAPI

app = FastAPI()

student = {"id": 1 , "name":"Messum" , "field_of_study":"Artificial Intelligence"}

@app.get("/student")
def get_student():
    return student