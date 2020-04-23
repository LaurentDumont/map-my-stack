FROM python:3.8.0b3-alpine3.10

RUN adduser -D map-my-stack

WORKDIR /home/map-my-stack

RUN apk --no-cache add build-base libressl-dev libffi-dev 

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY boot.sh ./
RUN chmod +x boot.sh

RUN chown -R map-my-stack:map-my-stack ./
USER map-my-stack

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
