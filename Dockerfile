FROM mongo:bionic
MAINTAINER Binghong wu <wubinhong2012@gmail.com>

# Timezone setting
ENV TZ="Asia/Shanghai"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Basic flask environment
COPY ./docker/sources.list /etc/apt/
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev curl nginx-full && rm -rf /var/lib/apt/lists/*
#RUN apt-get install -y build-essential

# Nginx component setting: redirect logger to container's std in/out which can be checkeout out via command docker logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# Sync app
RUN mkdir -p /app
COPY ./docker/requirements.txt /app
COPY ./docker/dict-entrypoint.sh /usr/local/bin
COPY ./backend/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000

# Health check
HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -fs http://localhost:5000 || exit 1

# Startup app
# Illustrate how to construct a standard dockefile, acutally, we don't have to use ENTRYPOINT here.
ENTRYPOINT ["dict-entrypoint.sh"]
CMD ["dict"]
