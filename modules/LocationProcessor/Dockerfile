FROM python:3.7-slim

WORKDIR .

RUN pip install pipenv && \
  apt-get update && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
  pipenv install --deploy --system && \
  apt-get remove -y gcc python3-dev libssl-dev && \
  apt-get autoremove -y && \
  pip uninstall pipenv -y \

COPY ./modules/LocationProcessor .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "run_location_processor.py"]