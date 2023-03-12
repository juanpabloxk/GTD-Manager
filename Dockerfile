# FROM python:3.10.8-alpine
FROM surnet/alpine-python-wkhtmltopdf:3.10.6-0.12.6-full

RUN mkdir /app

WORKDIR /app

RUN echo -e "#!/bin/sh\ncd /app && python3 main.py" > /etc/periodic/15min/run_app &&\
    chmod +rwx /etc/periodic/15min/run_app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . .

CMD ["crond","-f", "-l", "2"]
