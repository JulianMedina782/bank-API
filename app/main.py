from fastapi import FastAPI
from app.database import engine, Base 
from app.models import user 

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Bank API",       
    description= "API bancaria con Python, FastAPI y PostgreSQL",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bank API funcionando"}
