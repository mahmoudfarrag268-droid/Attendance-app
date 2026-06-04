<<<<<<< HEAD
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
=======
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
>>>>>>> fcfef4a18c3a4813d302a3bce133cf58882246bc
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]