FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache build-base gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY ./modules/PersonService .

RUN pip3 install -r requirements.txt

EXPOSE 5005 5001


CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]