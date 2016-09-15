
FROM tiangolo/uwsgi-nginx-flask:flask

RUN pip install reportlab
RUN pip install qrcode

COPY ./app /app

