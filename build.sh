#!/usr/bin/env bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -euxo pipefail

## Preparing before docker build
prepare_before_docker_build() {
    echo "Make preparing jobs before docker build:"
    echo "Clean up backend"
    (cd backend && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name *.pyc -exec rm -r {} +)
    echo "Build frontend page and package into dist"
    (cd frontend && npm install && npm run build)
}

## Remove container and image
container_name="dict_server1"
image_app="dict:v1"
image_base="dict:base"
remove_container() {
    echo "Remove container: ${container_name}"
    [ -z $(docker ps -aq -f "name=${container_name}") ] || docker container rm -f ${container_name}
}
remove_image_app() {
    remove_container
    echo "Remove image: ${image_app}"
    [ -z $(docker image ls -q ${image_app}) ] || docker image rm ${image_app}
}
remove_image_base() {
    remove_image_app
    echo "Remove image: ${image_base}"
    [ -z $(docker image ls -q ${image_base}) ] || docker image rm ${image_base}
}

## Main
### Go to directory this script belonged to
cd `dirname $0`
### Task
case "${1-''}" in
    image)
        echo "Building image task starting..."
        case "${2-''}" in
            base)
                remove_image_base
                echo "Build base image"
                docker build --target base -t ${image_base} -f Dockerfile .
                ;;
            app)
                echo "Start building image task..."
                prepare_before_docker_build
                remove_image_app
                echo "Build docker image for dict with tag: ${image_app}"
                docker build --target app -t ${image_app} -f Dockerfile .
                echo "Docker image <${image_app}> built successfully!"
                ;;
            *)
                echo "Usage: ./build.sh image <base|app>"
                ;;
        esac
        ;;
    container)
        remove_container
        echo "Start make container <${container_name}> ..."
        docker run --name ${container_name} -d -p 9000:80 -v /data/container/db:/data/db -v /data/container/configdb:/data/configdb ${image_app}
        echo "Container <${container_name}> made successfully!"
        ;;
    *)
        echo "Usage: ./build.sh <image <base|app>|container>"
        ;;
esac