FROM nikolaik/python-nodejs:python3.8-nodejs12-slim

RUN mkdir simple-login
COPY requirements.txt /simple-login
WORKDIR /simple-login
RUN pip install -r requirements.txt

# add unique index
RUN python manage.py migrate login

CMD ["python", "manage.py", "runserver", "8080"]