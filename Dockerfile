FROM python:3.8-slim-buster

# Install requirements in venv
RUN pip3 --disable-pip-version-check --no-cache-dir install -r ./requirements.txt

WORKDIR /code
COPY ./blast_ct /code



