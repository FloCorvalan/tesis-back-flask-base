FROM continuumio/miniconda3

WORKDIR /app

COPY ./req.txt /app/req.txt

COPY ./req2.txt /app/req2.txt

COPY /src /app

COPY .env /app

RUN conda create --name myenv --file req.txt

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]