FROM mongo:bionic AS base
LABEL author="Binghong wu" email="<wubinhong2012@gmail.com>"

# Timezone setting
ENV TZ="Asia/Shanghai"
# There are tree locales (C, C.UTF-8, POSIX) in image(mongo:bionic), so just take C.UTF-8 as default locale.
ENV LANG="C.UTF-8" LC_ALL="C.UTF-8" LC_LANG="C.UTF-8" PYTHONIOENCODING="UTF-8"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Basic flask environment
COPY ./docker/sources.list /etc/apt/
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev curl tree vim net-tools tcpdump iputils-ping traceroute atop glances cron nginx-full redis-server && rm -rf /var/lib/apt/lists/*
#RUN apt-get install -y build-essential

# Nginx component setting: redirect logger to container's std in/out which can be checkeout out via command docker logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
# Disable IPv6 for redis-server
RUN sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf

# Volume
VOLUME [ "/data" ]

### =================== New Stage =========================== ###
# Stage two building
FROM wbh/dict:base AS app
### =================== New Stage =========================== ###
# Parse argument
## Which frontend project we should deploy
ARG FRONTEND_PROJECT=frontend
# Sync app
RUN echo "FRONTEND_PROJECT: ${FRONTEND_PROJECT}" && mkdir -p /root/.pip
### $ tar -cJf node.tar.xz node or $ tar -c node | xz > node2.tar.xz

# Compile frontend file in docker image
## Install nodejs_12
# COPY ./docker/node.tar.xz /app/
# COPY ./docker/.npmrc /root/
# RUN cd /app && tar xf node.tar.xz && rm node.tar.xz
## Compile frontend project with nodejs
# COPY ./${FRONTEND_PROJECT} /app/src
# RUN (cd /app/src/ && export PATH=$PATH:/app/node/bin && npm install && npm run build && mv dist /app/frontend && rm -r /app/src)

# Copy compiled file from host directly, considering the fact that "npm install & build" takes a long time.
## This option which is mutually exclusive to the one commented above should be used in accordance with shell `build.sh`
COPY ./${FRONTEND_PROJECT}/dist /app/frontend

COPY ./backend /app/backend
COPY ./docker/pip-requirements.txt /app/backend/
## Configure pip
COPY ./docker/pip.conf /root/.pip/
COPY ./docker/dict-entrypoint.sh /usr/local/bin
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/dict.conf /etc/nginx/sites-available/default
COPY ./docker/cron_backup.sh /app
COPY ./docker/cron_task /etc/cron.d/backup-task

# Install python dependencies and set environment variables
WORKDIR /app/backend
ENV PYTHON_ENV=product
RUN pip3 install -r pip-requirements.txt
EXPOSE 5000

# Health check
HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -fs /backend/words/fuzzy?keyword=&skip=0&limit=1 || exit 1

# Startup app
# Illustrate how to construct a standard dockefile, acutally, we don't have to use ENTRYPOINT here.
ENTRYPOINT ["dict-entrypoint.sh"]
CMD ["dict"]
