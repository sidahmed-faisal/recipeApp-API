FROM python:3.9-alpine3.13
LABEL maintainer="Sidahmed"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# only to use the dev requirements by running docker compose
ARG DEV=false
#run the container with single layer of specifications
# create a virtual environment name py to avoid confilcts with docker image dependencies
RUN python -m venv /py && \
    # upgrade pip 
    /py/bin/pip install --upgrade pip && \ 
    # install postgresql-client to connect to the psycopg package
    apk add --update --no-cache postgresql-client &&\
    # group installed packages below to virtual environment named .tmp-build-deps 
    apk add --update --no-cache --virtual .tmp-build-deps \
    #  install 3 packages needed by the adapter
        build-base postgresql-dev musl-dev && \
    # install requirements file from the copied requirments file
    /py/bin/pip install -r /tmp/requirements.txt && \
    # install requirments.dev if DEV is true
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # remove temp files
    rm -rf /tmp && \
    # Delete packages group to keep a lightweight docker file
    apk del .tmp-build-deps &&\
    # add user to the container
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update the PATH environment variable to run executables from the venv's bin
ENV PATH="/py/bin:$PATH"

# specifies the user to switch to after running all commands
USER django-user
