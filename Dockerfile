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
RUN apt-get install -y python3-pip python3-dev curl tree cron nginx-full redis-server && rm -rf /var/lib/apt/lists/*
#RUN apt-get install -y build-essential

# Nginx component setting: redirect logger to container's std in/out which can be checkeout out via command docker logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
# Disable IPv6 for redis-server
RUN sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf

### =================== New Stage =========================== ###
# Stage two building
FROM dict:base AS app
### =================== New Stage =========================== ###
# Parse argument
## Which frontend project we should deploy
ARG FRONTEND_PROJECT=frontend
# Sync app
RUN echo "FRONTEND_PROJECT: $FRONTEND_PROJECT" && mkdir -p /app/backend /app/frontend
COPY ./$FRONTEND_PROJECT/dist/ /app/frontend/
COPY ./backend/ /app/backend/
COPY ./docker/pip-requirements.txt /app/backend
COPY ./docker/dict-entrypoint.sh /usr/local/bin
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
