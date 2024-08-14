FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libaio1 \
    libpq-dev \
    build-essential \
    wget \
    unzip

RUN wget https://download.oracle.com/otn_software/linux/instantclient/2350000/instantclient-basic-linux.x64-23.5.0.24.07.zip && \
    unzip instantclient-basic-linux.x64-23.5.0.24.07.zip && \
    rm instantclient-basic-linux.x64-23.5.0.24.07.zip && \
    mv instantclient_23_5 /opt/oracle

ENV LD_LIBRARY_PATH=/opt/oracle
ENV ORACLE_HOME=/opt/oracle

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download hr_core_news_sm
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
