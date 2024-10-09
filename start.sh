#!/bin/bash
if [ -z "$1" ]
then
    echo "No environment argument supplied, defaulting to dev"
    cp app/dev.env app/.env
else
    if [ $1 == "prod" ]
    then
        cp app/prod.env app/.env
    else
        cp app/dev.env app/.env
    fi
fi
while IFS= read -r line
do
    if [[ $line == *=* && $line != "#"* ]]; then
        name=$(echo $line | cut -d'=' -f1)
        export $name=$(echo $line | cut -d'=' -f2)
        echo $name=${!name}
    fi
done < app/.env
if [ -z "$1" ] || [ $1 != "prod" ]
then
    fastapi dev app/main.py
else
    fastapi run app/main.py
fi