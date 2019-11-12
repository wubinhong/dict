#!/usr/bin/env bash

## Launch mongodb
docker-entrypoint.sh mongod &
### Checkout whether mongod start up, the following coding copy from docker-entrypoint.sh in image mongo:bionic
mongoRes=( mongo --host 127.0.0.1 --port 27017 --quiet )
tries=30
while true; do
    if "${mongoRes[@]}" 'admin' --eval 'quit(0)' &> /dev/null; then
        # success!
        echo "Mongod launch successfully!"
        break
    fi
    echo "No response received from mongod and retry later: ${tries}"
    (( tries-- ))
    if [ "$tries" -le 0 ]; then
        echo >&2
        echo >&2 "error: mongod does not appear to have accepted connections quickly enough -- perhaps it had an error?"
        echo >&2
        exit 1
    fi
    sleep 1
done

## Launch nginx server
service nginx start

## Launch python app
originalArgOne="$1"
if [ "$originalArgOne" = 'dict' ]; then
    python3 /app/app.py
    #python3 /app/app.py 1>/data/out.log 2>/data/err.log
fi

exec "$@"