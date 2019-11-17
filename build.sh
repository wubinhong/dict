#!/usr/bin/env bash

## Preparing before docker build
prepare_before_docker_build() {
    echo "Make preparing jobs before docker build:"
    echo "Clean up backend"
    (cd backend && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name *.pyc -exec rm -r {} +)
    echo "Build frontend page and package into dist"
    (cd frontend && npm install && npm run build)
}

## Main
### Go to directory this script belonged to
cd `dirname $0`
### Task
case "$1" in
    image)
        echo "Start building image task..."
        prepare_before_docker_build
        echo "Build docker image for dict with tag: dict:v1"
        docker build -t dict:v1 -f Dockerfile .
        echo "Docker image <dict:v1> built successfully!"
        ;;
    container)
        echo "Start make container <dict_server1> ..."
        docker run --name dict_server1 -d -p 9000:80 -v /data/container/db:/data/db -v /data/container/configdb:/data/configdb dict:v1
        echo "Container <dict_server1> made successfully!"
        ;;
    clean)
        echo "Start clean task: remove container and image for rebuilding..."
        docker container rm -f dict_server1
        docker image rm dict:v1
        ;;
    *)
        echo "Usage: ./build.sh <image|container|clean>"
        ;;
esac