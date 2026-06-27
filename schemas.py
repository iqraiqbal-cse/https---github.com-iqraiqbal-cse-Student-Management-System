from pydantic import BaseModel

# Student ka data input lene ke liye schema
class StudentBase(BaseModel):
    name: str
    age: int
    course: str

# Student ka data response (output) me bhejne ke liye schema (isme ID bhi shamil hai)
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True