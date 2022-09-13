FROM python:3.8.10
# Заргружаем образ для python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Установка виртуальных переменных

WORKDIR /usr/src/dj
# Установка директории внутри контейнера, которая будет рабочей

COPY ./req.txt /usr/src/req.txt
RUN pip install --upgrade pip
RUN python3 -m pip install -r /usr/src/req.txt


COPY . /usr/src/dj


# EXPOSE 8000
CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]