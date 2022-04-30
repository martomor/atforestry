FROM python:3.8.1-slim
EXPOSE 8001
WORKDIR /app
COPY . /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt --no-cache-dir
CMD ["uvicorn","--host","0.0.0.0","--port", "8001", "api.main:app"]