FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install Django
RUN pip install django-bootstrap4
RUN pip install django-prometheus
RUN pip install Pillow
RUN pip install Faker

COPY . /app/

RUN python3 manage.py migrate
RUN python manage.py filling --db_size=small