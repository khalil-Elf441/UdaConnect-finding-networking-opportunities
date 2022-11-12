FROM python:3.7-slim

WORKDIR .

RUN pip install pipenv
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc python3-dev libssl-dev
RUN pipenv install --deploy --system
RUN apt-get remove -y gcc python3-dev libssl-dev
RUN apt-get autoremove -y
RUN pip uninstall pipenv -y

COPY ./modules/LocationProcessor .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "run_location_processor.py"]