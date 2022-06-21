FROM python:3.8-slim-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 list

COPY /src /app
COPY .env /app

ENTRYPOINT [ "python3.8" ]

CMD [ "-u", "app.py" ]