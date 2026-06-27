from sqlalchemy import Column, Integer, String
from database import Base

# Database me 'students' naam ki table banegi
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True) # Unique ID automatically banegi
    name = Column(String, nullable=False)              # Student ka naam
    age = Column(Integer, nullable=False)               # Student ki age
    course = Column(String, nullable=False)            # Course ka naam