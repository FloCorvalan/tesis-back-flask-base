FROM continuumio/miniconda3

WORKDIR /app

COPY ./req.txt /app/req.txt

COPY ./req2.txt /app/req2.txt

RUN conda create --name myenv --file req.txt

RUN conda activate myenv

RUN pip install -r req2.txt

COPY /src /app

COPY .env /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]