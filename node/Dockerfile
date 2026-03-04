FROM python:3.10-bullseye
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Certs
# RUN wget http://certs.provider.com/CERT_NAME.crt -O CERT_NAME.crt ; \
#     mv CERT_NAME.crt /usr/local/share/ca-certificates ; \
#     update-ca-certificates

# Requirements
RUN apt update ; apt install -y mosquitto

# CMD ["/bin/sh", "start.sh"]
CMD ["sleep", "infinity"]
