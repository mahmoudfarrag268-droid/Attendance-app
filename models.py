from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

# 1. جدول الموظفين (مكتوب مرة واحدة فقط وبشكل صحيح)
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    department = Column(String)

# 2. جدول الحضور والانصراف الجغرافي
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True)
    type = Column(String) 
    timestamp = Column(DateTime, default=datetime.utcnow)
    latitude = Column(String)
    longitude = Column(String)
    delay_minutes = Column(Integer, default=0) # الحقل الجديد لتخزين دقائق التأخير