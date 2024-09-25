# Python version can be changed, e.g.
# FROM python:3.8
# FROM ghcr.io/mamba-org/micromamba:1.5.1-focal-cuda-11.3.1
FROM docker.io/python:3.12.1-slim-bookworm

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="register_image" \
      org.opencontainers.image.description="This plugin re-orients a 3D scan (CT, MRI, PET, etc) into standard ' \
      ' planes, re-slices the re-oriented image, and saves the re-oriented images as a NIfTI file."

ARG SRCDIR=/usr/local/src/app
WORKDIR ${SRCDIR}

COPY requirements.txt .
RUN --mount=type=cache,sharing=private,target=/root/.cache/pip pip install -r requirements.txt

# ----------------------------------------------
# Install FSL:

python3 -m pip install --upgrade certifi
python3 -m certifi

echo "export SSL_CERT_FILE=$(python3 -m certifi)" >> ~/.bash_profile
source ~/.bash_profile


wget https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/releases/fslinstaller.py

chmod +x fslinstaller.py
python3 fslinstaller.py -q

echo "export FSLDIR=/usr/local/fsl" >> ~/.bash_profile
echo ". ${FSLDIR}/etc/fslconf/fsl.sh" >> ~/.bash_profile
echo "PATH=${FSLDIR}/bin:${PATH}" >> ~/.bash_profile
source ~/.bash_profile

# ----------------------------------------------


COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["commandname"]
