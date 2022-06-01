from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Employee(BaseModel):
    name: str = Field(min_length=1)


@app.get("/employees")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


@app.post("/employees")
def create_employee(employee: Employee, db: Session = Depends(get_db)):
    emp_model = models.Employee()
    emp_model.name = employee.name

    db.add(emp_model)
    db.commit()

    return employee


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp_model = (
        db.query(models.Employee)
        .filter(models.Employee.employee_id == employee_id)
        .first()
    )

    if emp_model is None:
        raise HTTPException(
            status_code=404, detail=f"ID {employee_id} : Does not exist"
        )

    return emp_model
