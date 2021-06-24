FROM python:3.8
# MAINTAINER CRISTIAN_CONTRERA <cristiancontrera95@gmail.com>

#### sql server drives
RUN apt-get update && apt-get install curl

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get install -y unixodbc-dev
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev

ENV PATH="${PATH}:/opt/mssql-tools/bin:/opt/mssql-tools/bin"

WORKDIR /app

RUN pip install --upgrade pip

### Uncomment for usage
# COPY requirements.txt /app/requirements.txt
# RUN pip install -r requirements.txt

# COPY src/ ./

# EXPOSE 5000

# CMD ["python", "main.py"]
