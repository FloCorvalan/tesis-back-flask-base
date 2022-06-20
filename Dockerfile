FROM continuumio/miniconda:latest

WORKDIR /app

COPY environment.yml ./
COPY /src /app
COPY .env /app

RUN conda env create -f environment.yml

RUN echo "source activate myenv" > ~/.bashrc
ENV PATH /opt/conda/envs/myenv/bin:$PATH

RUN pip install -r req2.txt

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]