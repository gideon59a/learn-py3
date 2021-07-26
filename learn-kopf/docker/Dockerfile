# from https://kopf.readthedocs.io/en/latest/deployment/
FROM python:3.7
ADD . /src
RUN pip install kopf kubernetes
ENV workdir /src
WORKDIR ${workdir}
CMD kopf run khandler.py --verbose