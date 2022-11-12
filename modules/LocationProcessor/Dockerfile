FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev python3 py3-pip py-pip

COPY ./modules/LocationProcessor .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "run_location_processor.py"]