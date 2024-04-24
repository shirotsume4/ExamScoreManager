FROM python:3.9-slim

WORKDIR /src

COPY ./src/requirements.txt .
RUN pip install python-multipart
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./src/ .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]