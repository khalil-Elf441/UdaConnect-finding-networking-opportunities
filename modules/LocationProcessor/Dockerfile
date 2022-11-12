FROM python:3.7-alpine

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev

COPY ./modules/LocationProcessor .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "run_location_processor.py"]