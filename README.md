# dict
dict for IELTS preparation

## Dev mode




## Product mode with docker
- Build docker image dict:v1 with Dockerfile and take current directory build context directory
```bash
$ docker build -t dict:v1 -f Dockerfile .
```
- Build container with image built above
```bash
$ docker run --name dict_server1 -d -p 8088:5000 dict:v1
```
- Checkout container
```bash
$ docker container ls
```
- Healthy check
```bash
$ curl -iv http://localhost:8088
```
- Container log info checking
```bash
$ docker logs dict_server1
```
- Login container with bash: It's convenient to checkout the inner content of the container. It's useful when we debuging the docker images.
```bash
$ docker exec -it dict_server1 bash 
```




