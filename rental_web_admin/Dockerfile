FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /rental_web_admin

ADD . /rental_web_admin

ENTRYPOINT ["python", "manage.py"]

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8005

CMD ["runserver", "0.0.0.0:8005"]
