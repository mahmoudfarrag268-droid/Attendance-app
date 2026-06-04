<<<<<<< HEAD
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تحديد اسم ومكان ملف قاعدة البيانات
SQLALCHEMY_DATABASE_URL = "sqlite:///./attendance.db"

# إنشاء محرك قاعدة البيانات
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# إنشاء جلسة للتعامل مع البيانات (إضافة، تعديل، حذف)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الأساس الذي سنبني عليه جداولنا برمجياً
=======
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تحديد اسم ومكان ملف قاعدة البيانات
SQLALCHEMY_DATABASE_URL = "sqlite:///./attendance.db"

# إنشاء محرك قاعدة البيانات
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# إنشاء جلسة للتعامل مع البيانات (إضافة، تعديل، حذف)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الأساس الذي سنبني عليه جداولنا برمجياً
>>>>>>> fcfef4a18c3a4813d302a3bce133cf58882246bc
Base = declarative_base()