FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev

COPY ./modules/ConnectionService .

RUN pip install -r requirements.txt

EXPOSE 5003

CMD ["flask", "run", "--host", "0.0.0.0"]