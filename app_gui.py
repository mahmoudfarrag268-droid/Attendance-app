import tkinter as tk
from tkinter import messagebox
import requests

# رابط السيرفر الخاص بنا
API_URL = "http://127.0.0.1:8000/record-attendance/"

def send_attendance(action):
    emp_id = entry_id.get()
    if not emp_id:
        messagebox.showerror("خطأ", "برجاء إدخال الرقم الوظيفي أولاً!")
        return
    
    # إحداثيات تجريبية (موقع الشركة لتجربة النجاح)
    # يمكنك تغييرها لـ "30.0" لتجربة الرفض والسياج الجغرافي
    my_lat = "29.9526"
    my_lng = "30.9219"
    
    # إرسال البيانات للسيرفر المطور
    params = {
        "employee_id": emp_id,
        "action_type": action,
        "lat": my_lat,
        "lng": my_lng
    }
    
    try:
        response = requests.post(API_URL, params=params)
        result = response.json()
        
        if response.status_code == 200:
            messagebox.showinfo("نجاح العملية", result["message"])
        else:
            messagebox.showwarning("تم رفض الطلب", result["detail"])
    except:
        messagebox.showerror("خطأ في الاتصال", "تأكد من تشغيل سيرفر بايثون أولاً!")

# بناء واجهة النافذة
root = tk.Tk()
root.title("نظام الحضور الذكي - بوابة الموظف")
root.geometry("400x250")
root.configure(bg="#f0f4f8")

# العناصر المرئية
tk.Label(root, text="نظام الحضور والانصراف الجغرافي", font=("Arial", 14, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)

tk.Label(root, text="أدخل الرقم الوظيفي:", font=("Arial", 10), bg="#f0f4f8").pack()
entry_id = tk.Entry(root, font=("Arial", 12), justify="center")
entry_id.pack(pady=5)

# أزرار التشغيل
btn_frame = tk.Frame(root, bg="#f0f4f8")
btn_frame.pack(pady=20)

btn_in = tk.Button(btn_frame, text="تسجيل دخول (Check In)", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), command=lambda: send_attendance("دخول"))
btn_in.pack(side="left", padx=10)

btn_out = tk.Button(btn_frame, text="تسجيل خروج (Check Out)", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), command=lambda: send_attendance("خروج"))
btn_out.pack(side="right", padx=10)

root.mainloop()