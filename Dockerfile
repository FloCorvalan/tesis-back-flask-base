FROM continuumio/miniconda:latest

WORKDIR /app

COPY environment.yml ./
COPY /src /app
COPY .env /app

RUN sleep 30; conda env create -f environment.yml

RUN echo "source activate myenv" > ~/.bashrc
ENV PATH /opt/conda/envs/myenv/bin:$PATH

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]