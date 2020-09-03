FROM python:3.8
RUN pip install kubernetes

WORKDIR /code

COPY src/ .

CMD ["python", "./sidecar.py"]
