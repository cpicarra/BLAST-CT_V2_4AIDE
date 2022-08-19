FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

ARG PYTHON_VERSION=3.9

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /code
RUN cd /code \
    && apt-get update && apt-get install -y git wget unzip nano
ADD https://api.github.com/repos/cpicarra/BLAST-CT_V2_4AIDE/git/refs/heads/localisation_foraide version.json
RUN git clone -b localisation_foraide https://github.com/cpicarra/BLAST_CT_V2_4AIDE.git
RUN ls /code/BLAST_CT_V2_4AIDE
RUN pip3 --disable-pip-version-check --no-cache-dir install -r ./BLAST_CT_V2_4AIDE/requirements.txt
WORKDIR /code/BLAST_CT_V2_4AIDE
