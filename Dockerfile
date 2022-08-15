FROM python:3.8-slim-buster
WORKDIR /code
RUN cd /code
RUN apt-get update && apt-get install -y git wget unzip nano
# ADD https://api.github.com/repos/cpicarra/BLAST-CT_V2_4AIDE/git/refs/heads/localisation_foraide version.json
RUN git clone -b localisation_foraide https://github.com/cpicarra/BLAST-CT_V2_4AIDE.git
RUN pip3 --disable-pip-version-check --no-cache-dir install -r ./blast_ct/requirements.txt
# COPY image.nii.gz /tmp/image.nii.gz

