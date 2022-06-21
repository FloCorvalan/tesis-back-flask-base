FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y aptitude && \
    aptitude install -y build-essential  && \
    apt-get install -y wget && \
    apt-get install -y zlib1g-dev && \
    apt-get install -y libncurses5-dev && \
    apt-get install -y libgdbm-dev && \
    apt-get install -y libnss3-dev && \
    apt-get install -y libssl-dev && \
    apt-get install -y libreadline-dev && \
    apt-get install -y libffi-dev && \
    apt-get install -y libsqlite3-dev && \
    apt-get install -y libbz2-dev

RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz

RUN tar -xf Python-3.8.5.tgz

RUN cd Python-3.8.5 && \
    ./configure --enable-optimizations && \
    make -j 8 && \
    make altinstall

RUN python3.8 --version

RUN apt-get update -y && \
    apt-get install -y python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 list

COPY /src /app
COPY .env /app

ENTRYPOINT [ "python3.8" ]

CMD [ "app.py" ]