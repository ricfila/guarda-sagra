FROM python

WORKDIR /home/guarda-sagra

COPY . .

RUN ["python", "-m", "pip", "install", "dist/guarda_sagra-0.0.1-py3-none-any.whl"]

ENV PYTHONPATH /home/guarda-sagra

EXPOSE 5000 5432

ENTRYPOINT ["guarda-sagra"]
