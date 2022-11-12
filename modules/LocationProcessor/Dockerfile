FROM python:3.8-alpine

WORKDIR .

RUN apk add --no-cache gcc g++ python3-dev python3 py3-pip

COPY ./modules/LocationProcessor .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "run_location_processor.py"]