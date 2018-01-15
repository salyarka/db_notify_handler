#!/usr/bin/env bash

if [ "$APP_CONFIG" == "dev" ] || [ "$APP_CONFIG" == "prod" ]; then
    python run.py start
elif [ "$APP_CONFIG" == "test" ]; then
    python run.py test

else
    echo -e "\033[0;31mAPP_CONFIG variable is not defined!\033[0m"
fi
