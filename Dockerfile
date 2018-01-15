FROM python:3.6.1

ARG APP_CONFIG

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install requirements
ADD requirements /usr/src/app/requirements
RUN pip install -r requirements/${APP_CONFIG}.txt

# add app
ADD . /usr/src/app

# launch script
CMD ./docker-entrypoint.sh
