
FROM tiangolo/uwsgi-nginx-flask:flask

RUN pip install reportlab

COPY ./app /app

