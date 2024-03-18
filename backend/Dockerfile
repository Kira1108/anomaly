FROM python:3.10-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat-traditional gcc \
  && apt-get clean \
  && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir -U pip && pip install setuptools wheel

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host 0.0.0.0", "--port 8000","--reload"]