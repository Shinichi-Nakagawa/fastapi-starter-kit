FROM python:3.8

LABEL  maintainer "Shinichi Nakagawa <spirits.is.my.rader@gmail.com>"

# install
COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install

# app
COPY app.py db.py ./
ADD book book
RUN python db.py