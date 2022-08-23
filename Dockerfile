FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

ARG PYTHON_VERSION=3.9

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install libjpeg-dev zlib1g-dev git -y

WORKDIR /code
RUN cd /code
RUN apt-get update && apt-get install -y git wget unzip nano
ADD https://api.github.com/repos/cpicarra/BLAST-CT_V2_4AIDE/git/refs/heads/localisation_foraide version.json
RUN git clone -b localisation_foraide https://github.com/cpicarra/BLAST_CT_V2_4AIDE.git
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /code/BLAST_CT_V2_4AIDE/requirements.txt
WORKDIR /code/BLAST_CT_V2_4AIDE
# CMD python3

