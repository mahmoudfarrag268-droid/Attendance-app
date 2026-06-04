from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse # استيراد لدعم صفحات الويب
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
import math 
from datetime import datetime, time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return c * 6371000

@app.get("/attendance-report/")
def get_attendance_report(db: Session = Depends(get_db)):
    return db.query(models.Attendance).all()

@app.post("/add-employee/")
def add_employee(employee_id: str, name: str, department: str, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="مسجل مسبقاً!")
    new_employee = models.Employee(employee_id=employee_id, name=name, department=department)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {"status": "success", "message": f"تم تسجيل الموظف {name} بنجاح!"}

@app.post("/record-attendance/")
def record_attendance(employee_id: str, action_type: str, lat: str, lng: str, db: Session = Depends(get_db)):
    employee_exists = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee_exists:
        raise HTTPException(status_code=404, detail="هذا الموظف غير مسجل!")
    
    COMPANY_LAT = 29.9526
    COMPANY_LNG = 30.9219
    ALLOWED_RADIUS = 100 
    
    distance = calculate_distance(lat, lng, COMPANY_LAT, COMPANY_LNG)
    if distance > ALLOWED_RADIUS:
        raise HTTPException(status_code=400, detail=f"أنت خارج النطاق الجغرافي للشركة بـ {round(distance)} متر.")
    
    delay = 0
    if action_type == "دخول":
        current_time = datetime.now().time()
        work_start_time = time(9, 0)
        if current_time > work_start_time:
            full_date_1 = datetime.combine(datetime.today(), current_time)
            full_date_2 = datetime.combine(datetime.today(), work_start_time)
            delay = int((full_date_1 - full_date_2).total_seconds() / 60)

    new_record = models.Attendance(
        employee_id=employee_id, type=action_type, latitude=lat, longitude=lng, delay_minutes=delay
    )
    db.add(new_record)
    db.commit()
    
    msg = f"تم تسجيل {action_type} بنجاح."
    if delay > 0:
        msg += f" تنبيه: لديك تأخير {delay} دقيقة!"
    return {"status": "success", "message": msg}

# --- الدالة الجديدة التي تعرض صفحة الويب للموظفين عند فتح الرابط الأساسي ---
@app.get("/", response_class=HTMLResponse)
def employee_interface():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>بوابة الحضور الذكي</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f7f6; text-align: center; padding: 30px; }
            .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
            input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 6px; text-align: center; font-size: 16px; }
            button { width: 45%; padding: 12px; margin: 10px 2%; border: none; border-radius: 6px; color: white; font-size: 16px; cursor: pointer; font-weight: bold; }
            .btn-in { background-color: #2ecc71; }
            .btn-out { background-color: #e74c3c; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>نظام الحضور الجغرافي</h2>
            <p>برجاء إدخال رقمك الوظيفي لتسجيل الحضور أو الانصراف</p>
            <input type="text" id="empId" placeholder="مثال: EMP101">
            <br>
            <button class="btn-in" onclick="sendData('دخول')">تسجيل دخول</button>
            <button class="btn-out" onclick="sendData('خروج')">تسجيل خروج</button>
        </div>

        <script>
            function sendData(action) {
                const empId = document.getElementById('empId').value;
                if(!empId) { alert('برجاء كتابة الرقم الوظيفي أولاً!'); return; }
                
                // طلب إحداثيات الـ GPS الحقيقية من متصفح الهاتف
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    // إرسال البيانات للسيرفر
                    const url = `/record-attendance/?employee_id=${empId}&action_type=${action}&lat=${lat}&lng=${lng}`;
                    fetch(url, { method: 'POST' })
                    .then(res => res.json())
                    .then(data => {
                        if(data.detail) { alert('فشل: ' + data.detail); }
                        else { alert('نجاح: ' + data.message); }
                    })
                    .catch(err => alert('خطأ في الاتصال بالسيرفر'));
                }, function(err) {
                    alert('برجاء تفعيل الـ GPS في هاتفك لتتمكن من تسجيل الحضور!');
                });
            }
        </script>
    </body>
    </html>
    """