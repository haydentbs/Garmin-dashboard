FROM python:3.10-slim

WORKDIR /aop

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    libpq-dev 

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]