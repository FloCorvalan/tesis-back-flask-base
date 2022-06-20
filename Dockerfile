FROM continuumio/miniconda3

WORKDIR /app

COPY ./req.txt /app/req.txt

RUN conda create --name myenv --file req.txt

RUN conda activate myenv

COPY /src /app

COPY .env /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]