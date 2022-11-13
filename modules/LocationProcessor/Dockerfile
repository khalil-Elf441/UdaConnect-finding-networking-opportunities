FROM python:3.8

WORKDIR .

COPY ./modules/LocationProcessor .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "run_location_processor.py"]