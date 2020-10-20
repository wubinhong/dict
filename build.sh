#!/usr/bin/env bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -euxo pipefail

## Variables settings
frontend_project="${3-mobile}"

## Preparing before docker build
prepare_before_docker_build() {
    echo "Make preparing jobs before docker build:"
    echo "Clean up backend"
    (cd backend && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name *.pyc -exec rm -r {} +)
    echo "Build frontend page <${frontend_project}> and package into dist"
    (cd ${frontend_project} && npm install && npm run build)
}

## Remove container and image
container_name="dict_server1"
image_app="wbh/dict:v1"
image_base="wbh/dict:base"
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
                docker build --target app -t ${image_app} --build-arg FRONTEND_PROJECT=${frontend_project} -f Dockerfile .
                echo "Docker image <${image_app}> built successfully!"
                ;;
            *)
                echo "Usage: ./build.sh image <base|app [frontend|mobile]>"
                ;;
        esac
        ;;
    container)
        remove_container
        echo "Start make container <${container_name}> ..."
        docker run --name ${container_name} -d -p 9000:80 -v ~/data/container/dict:/data -v ~/data/container/dict/db:/data/db ${image_app}
        echo "Container <${container_name}> made successfully!"
        ;;
    compose)
        echo "Launching docker-compose..."
        case "${2-''}" in
            build)
                prepare_before_docker_build
                docker-compose build
                ;;
            up)
                prepare_before_docker_build
                docker-compose up -d --build
                ;;
            down)
                docker-compose down
                ;;
            logs)
                docker-compose logs -f
                ;;
            *)
                echo "Usage: ./build.sh compose <build|up|down|logs>"
                ;;
        esac
        ;;
    *)
        echo "Usage: ./build.sh <image|compose>"
        ;;
esac