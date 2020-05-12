FROM python:3.8-slim

RUN apt update && apt -y upgrade && apt install -y gcc

COPY src /app/src

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app

CMD ["python", "-m", "src.main"]
#CMD ["python", "-m", "src.common.logs_subscriber", "login"]
#CMD ["python", "-m", "src.common.logs_subscriber", "metrics"]
#CMD ["python", "-m", "src.common.logs_subscriber", "logs"]
