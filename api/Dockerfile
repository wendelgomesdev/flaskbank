FROM python:3.8-slim

COPY . /app

WORKDIR /app
  
RUN apt-get update && apt-get install

RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]