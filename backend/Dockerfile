FROM python:3.10

WORKDIR /opt/auth

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY ./src .

EXPOSE 5000

COPY script.sh /

RUN chmod +x /script.sh

ENTRYPOINT ["/script.sh"]