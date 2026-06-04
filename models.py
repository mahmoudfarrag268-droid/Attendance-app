<<<<<<< HEAD
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
=======
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
>>>>>>> fcfef4a18c3a4813d302a3bce133cf58882246bc
