FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip

RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev 

RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz

RUN tar -xf Python-3.8.5.tgz && cd Python-3.8.0 && ./configure --enable-optimizations && make -j 8 && make altinstall

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY /src /app

COPY .env /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]