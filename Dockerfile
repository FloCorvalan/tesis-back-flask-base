FROM continuumio/miniconda3

WORKDIR /app

COPY ./req.txt /app/req.txt

COPY ./req2.txt /app/req2.txt

RUN conda create --name myenv --file req.txt

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

RUN pip install -r req2.txt

COPY /src /app

COPY .env /app

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python"]

CMD [ "app.py" ]