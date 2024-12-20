FROM python:3.9-slim-buster

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code

# Set PYTHONPATH to include /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

ENV FLASK_APP=runner.entrypoints.flask_app FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80