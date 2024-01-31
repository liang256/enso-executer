FROM python:3.9-slim-buster

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code

# Set PYTHONPATH to include /code
ENV PYTHONPATH "${PYTHONPATH}:/code"

CMD tail -f /dev/null
