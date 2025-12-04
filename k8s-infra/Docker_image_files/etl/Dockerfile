FROM python:alpine3.21

WORKDIR /app

COPY etl.py /app/etl.py

RUN pip install requests

CMD ["python", "/app/etl.py"]
