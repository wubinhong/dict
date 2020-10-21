#!/usr/bin/env bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -euxo pipefail

## Variables settings
frontend_project="${2-mobile}"

## Preparing before docker build
prepare_before_docker_build() {
    echo "Make preparing jobs before docker build:"
    echo "Clean up backend"
    (cd backend && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name *.pyc -exec rm -r {} +)
    echo "Build frontend page <${frontend_project}> and package into dist"
    (cd ${frontend_project} && npm install && npm run build)
}

## Main
### Go to directory this script belonged to
cd `dirname $0`
### Task
case "${1-''}" in
    build)
        # prepare_before_docker_build
        docker-compose build
        ;;
    up)
        # prepare_before_docker_build
        docker-compose up -d --build
        ;;
    down)
        docker-compose down
        ;;
    logs)
        docker-compose logs -f
        ;;
    *)
        echo "Usage: ./build.sh <build|up|down|logs>"
        ;;
esac