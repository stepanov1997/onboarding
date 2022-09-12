FROM python:slim

RUN apt-get update || exit 1
RUN apt-get install -y curl tar awscli gcc g++ libsasl2-dev libsasl2-2 libsasl2-modules-gssapi-mit || exit 1
RUN apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY script.py script.py

ENTRYPOINT ["python3"]
CMD ["script.py","run"]