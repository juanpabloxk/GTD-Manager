FROM python:3.10.8-alpine

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/requirements.app

COPY entrypoint.sh /entrypoint.sh

RUN ["chmod", "+x", "/entrypoint.sh"]

RUN pip install -r /app/requirements.app

COPY . .

ENTRYPOINT ["/entrypoint.sh"]

CMD ["crond","-f", "-l", "2"]
