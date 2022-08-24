FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

ARG PYTHON_VERSION=3.9

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install libjpeg-dev zlib1g-dev git -y
WORKDIR /code
RUN cd /code
RUN pip3 install git+https://github.com/cpicarra/BLAST_CT_V2_4AIDE.git#localisation_foraide

# CMD ["blast-ct-inference"]
