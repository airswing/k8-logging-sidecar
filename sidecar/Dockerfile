FROM python:3.8
RUN pip install kubernetes python-logstash

WORKDIR /code
COPY src/ .
COPY config.json ./config/config.json

CMD ["python", "./sidecar.py", "config/config.json"]

