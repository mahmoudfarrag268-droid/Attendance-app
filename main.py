from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    department = Column(String)
    work_lat = Column(Float, nullable=True)  # خط العرض للموقع المخصص
    work_lng = Column(Float, nullable=True)  # خط الطول للموقع المخصص

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True)
    type = Column(String)  # دخول أو خروج
    latitude = Column(Float)
    longitude = Column(Float)
    delay_minutes = Column(Integer, default=0)
    timestamp = Column(DateTime, default=DateTime) # سيتم تسجيل الوقت تلقائياً عند الإدخال