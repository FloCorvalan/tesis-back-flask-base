FROM conda/miniconda3

RUN conda config --set pip_interop_enabled false

COPY ./req.txt /app/req.txt

COPY ./req2.txt /app/req2.txt

WORKDIR /app

RUN conda create --name myenv --file req.txt

ENV PATH /opt/conda/envs/condaenv/bin:$PATH

SHELL ["/bin/bash", "-c"]

RUN conda activate myenv

RUN pip install -r req2.txt

COPY /src /app

COPY .env /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]