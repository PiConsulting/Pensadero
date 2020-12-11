FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

#MAINTAINER CRISTIAN_CONTRERA <cristiancontrera95@gmail.com>

WORKDIR /app

RUN apk update
# Install libraries for requirements
RUN apk add curl gcc g++ python3-dev libc-dev libffi-dev libxml2 unixodbc-dev>=2.3.6 openssl-dev

# Install ODBC driver for SQL Server
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.6.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.6.1.1-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql17_17.6.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.6.1.1-1_amd64.apk


COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# docker build -t folpix-api . ; docker run -p 8000:80 folpix-api
