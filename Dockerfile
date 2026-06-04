FROM python:3.10-slim

WORKDIR /app

# تثبيت التحديثات والأدوات الأساسية التي قد تحتاجها بعض المكتبات مثل opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات أولاً لتسريع البناء
COPY requirements.txt .

# تثبيت مكتبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع إلى السيرفر
COPY . .

# تشغيل تطبيق FastAPI باستخدام uvicorn على المنفذ 7860 (المنفذ الافتراضي لـ Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]