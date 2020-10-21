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
# Stage two building. Note: 使用docker-compose后，因为有了自己的cache机制，stage这种避免重复构建的办法已经用不上了
# FROM wbh/dict:base AS app
### =================== New Stage =========================== ###
# Parse argument
## Which frontend project we should deploy
ARG FRONTEND_PROJECT=frontend
# Sync app
RUN echo "ARG print and make directories. FRONTEND_PROJECT: ${FRONTEND_PROJECT}" && mkdir -p /app/src /root/.pip /app/backend

# Install nodejs_12 and install project
## $ tar -cJf node.tar.xz node or $ tar -c node | xz > node2.tar.xz
COPY ./docker/node.tar.xz /app/
COPY ./docker/.npmrc /root/
RUN cd /app && tar xf node.tar.xz && rm node.tar.xz
## Note: Docker's cache process will be utilized by separating "npm install" and "npm build" so as to avoid unnessary building process
COPY ./${FRONTEND_PROJECT}/package.json /app/src/
COPY ./${FRONTEND_PROJECT}/package-lock.json /app/src/
RUN cd /app/src/ && export PATH=$PATH:/app/node/bin && npm install

## Configure pip
COPY ./docker/pip.conf /root/.pip/
COPY ./docker/pip-requirements.txt /app/backend/
# Install python dependencies
RUN pip3 install -r /app/backend/pip-requirements.txt
COPY ./docker/dict-entrypoint.sh /usr/local/bin
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/dict.conf /etc/nginx/sites-available/default
COPY ./docker/cron_backup.sh /app
COPY ./docker/cron_task /etc/cron.d/backup-task

# Update app related files
WORKDIR /app
## Update frontend: Compile frontend project with nodejs in docker image
COPY ./${FRONTEND_PROJECT} /app/src
RUN cd /app/src/ && export PATH=$PATH:/app/node/bin && npm run build && mv dist /app/frontend && rm -r /app/src
## Update backend. Note: The longer the layer takes, the foremost the direct should be due to saving time.
COPY ./backend /app/backend
EXPOSE 5000

# Health check
HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -fs /backend/words/fuzzy?keyword=&skip=0&limit=1 || exit 1

# Startup app
# Illustrate how to construct a standard dockefile, acutally, we don't have to use ENTRYPOINT here.
ENTRYPOINT ["dict-entrypoint.sh"]
CMD ["dict"]
