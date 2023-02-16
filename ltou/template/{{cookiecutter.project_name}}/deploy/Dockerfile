FROM python:3.10.10-slim-buster
RUN apt-get update && apt-get install -y \
  gcc build-essential   vim-tiny\
  && rm -rf /var/lib/apt/lists/*

{%- if cookiecutter.db_info.name == "mysql" %}
RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}

 # postgresql postgresql-contrib libpq-dev
{%- if cookiecutter.db_info.name == "postgresql" %}
RUN apt-get update && apt-get install -y libpq-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*
{%- endif %}


RUN pip install poetry

# Configuring poetry
RUN poetry config virtualenvs.create false

## Copying requirements of a project
#COPY pyproject.toml poetry.lock /app/src/
#WORKDIR /app/src
#
## Installing requirements
#RUN poetry install
## Removing gcc
#RUN apt-get purge -y \
#  gcc \
#  && rm -rf /var/lib/apt/lists/*
#
## Copying actuall application
#COPY . /app/src/
#RUN poetry install
#
#CMD ["/usr/local/bin/python", "-m", "demofapi"]
