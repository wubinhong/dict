# Dict

dict for IELTS preparation

## Dev mode

## Product mode with docker

- Build docker image dict:v1 with Dockerfile and take current directory build context directory.

> Note: This process will be expected to be done at the host server.

```bash
(cd backend && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name *.pyc -exec rm -r {} +)
(cd frontend && npm install && npm run build)
docker build -t dict:v1 -f Dockerfile .
```

- Build container with image built above.
>
> * We specify the virtual volume for app logger output(`_host_local_directory_:_container_volume_`).
> * Volume definition /data/db and /data/configdb inherited from parent image mongo:bionic
> * Note: We usually do this process at the target server where the app run.
>
```bash
docker run --name dict_server1 -d -p 9000:80 -v /data/container/db:/data/db -v /data/container/configdb:/data/configdb dict:v1
```

> **Importance: A `build.sh` shell script was written to make building work more convenient.**

```bash
./build <image|container|clean>
```

- Checkout container

```bash
docker container ls
```

- Healthy check

```bash
curl -iv http://localhost:8088
```

- Container log info checking

```bash
docker logs dict_server1
```

- Login container with bash: It's convenient to checkout the inner content of the container. It's useful when we debuging the docker images.

```bash
docker exec -it dict_server1 bash
```

## Userful command line

- Delete all __pycache__ directory

```bash
find . -type d -name __pycache__ -exec rm -r {} +
```

## Reference docs

[vuejs](https://vuejs.org/v2/guide/)
[element-ui](https://element.eleme.cn/#/zh-CN)
