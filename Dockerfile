FROM python:3.8

COPY src /app/src

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 8000

WORKDIR /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]