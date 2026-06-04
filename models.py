from sqlalchemy import Column, Integer, String, Float
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    # هذا السطر يحل المشكلة ويسمح بتعديل الجدول دون أخطاء
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    department = Column(String)
    work_lat = Column(Float, nullable=True) 
    work_lng = Column(Float, nullable=True)

class Attendance(Base):
    __tablename__ = "attendance"
    # هذا السطر يحل المشكلة ويسمح بتعديل الجدول دون أخطاء
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String)
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    delay_minutes = Column(Integer)