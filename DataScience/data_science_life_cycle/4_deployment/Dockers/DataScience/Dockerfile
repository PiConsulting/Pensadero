FROM python:3.8-alpine
# MAINTAINER CRISTIAN_CONTRERA <cristiancontrera95@gmail.com>

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

### Uncomment for usage
# COPY main.py .

# EXPOSE 5000

# CMD ['python', 'main.py']
