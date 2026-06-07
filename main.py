from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal
import math 
from datetime import datetime
import traceback

# سيقوم بإنشاء ملف attendance.db الجديد كلياً بجميع الأعمدة المحدثة فوراً
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database Creation Error: {str(e)}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AttendanceRequest(BaseModel):
    employee_id: str
    action_type: str
    lat: float
    lng: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return c * 6371000
    except Exception:
        return 999999

@app.get("/attendance-report/")
def get_attendance_report(db: Session = Depends(get_db)):
    return db.query(models.Attendance).all()

@app.post("/add-employee/")
def add_employee(employee_id: str, name: str, department: str, work_lat: float, work_lng: float, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="مسجل مسبقاً!")
    
    new_employee = models.Employee(
        employee_id=employee_id, name=name, department=department, work_lat=work_lat, work_lng=work_lng
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {"status": "success", "message": f"تم تسجيل الموظف {name} بنجاح!"}

@app.post("/record-attendance/")
def record_attendance(data: AttendanceRequest, db: Session = Depends(get_db)):
    try:
        # 1. التحقق من الموظف في قاعدة البيانات
        employee = db.query(models.Employee).filter(models.Employee.employee_id == data.employee_id).first()
        if not employee:
            return {"status": "error", "message": "هذا الرقم الوظيفي غير مسجل في النظام!"}
        
        if employee.work_lat is None or employee.work_lng is None:
            return {"status": "error", "message": "لم يتم تحديد موقع عمل مخصص لهذا الموظف!"}
        
        # 2. حساب المسافة
        ALLOWED_RADIUS = 200 
        distance = calculate_distance(data.lat, data.lng, employee.work_lat, employee.work_lng)
        
        if distance > ALLOWED_RADIUS:
            return {"status": "error", "message": f"أنت خارج النطاق الجغرافي بـ {round(distance)} متر."}
        
        # 3. حساب التأخير
        delay = 0
        if data.action_type == "دخول":
            now = datetime.now()
            current_minutes = now.hour * 60 + now.minute
            work_start_minutes = 9 * 60  
            if current_minutes > work_start_minutes:
                delay = current_minutes - work_start_minutes

        # 4. حفظ السجل
        new_record = models.Attendance(
            employee_id=data.employee_id, 
            type=data.action_type, 
            latitude=float(data.lat), 
            longitude=float(data.lng), 
            delay_minutes=int(delay)
        )
        db.add(new_record)
        db.commit()
        
        msg = f"تم تسجيل {data.action_type} بنجاح!"
        if delay > 0:
            msg += f" (تأخير {delay} دقيقة)"
        return {"status": "success", "message": msg}

    except Exception as e:
        # التقاط أي خطأ خفي وإرساله كـ نص واضح بدلاً من انهيار السيرفر
        error_details = traceback.format_exc()
        print(error_details)  # ستظهر في الـ Logs الخاصة بالمنصة
        return {"status": "server_crash", "message": f"عطل داخلي في السيرفر: {str(e)}"}

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
                
                navigator.geolocation.getCurrentPosition(function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    const url = window.location.origin + "/record-attendance/";
                    
                    fetch(url, { 
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            employee_id: empId,
                            action_type: action,
                            lat: parseFloat(lat),
                            lng: parseFloat(lng)
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        // عرض الرسالة القادمة من السيرفر مباشرة سواء كانت نجاح أو تفاصيل العطل
                        alert(data.message);
                    })
                    .catch(err => {
                        alert('خطأ في الاتصال بالشبكة: ' + err.message);
                    });
                }, function(err) {
                    alert('برجاء تفعيل الـ GPS وصلاحية الموقع في المتصفح لتتمكن من تسجيل الحضور!');
                });
            }
        </script>
    </body>
    </html>
    """