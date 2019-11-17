FROM mongo:bionic
MAINTAINER Binghong wu <wubinhong2012@gmail.com>

# Timezone setting
ENV TZ="Asia/Shanghai"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Basic flask environment
COPY ./docker/sources.list /etc/apt/
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev curl tree nginx-full && rm -rf /var/lib/apt/lists/*
#RUN apt-get install -y build-essential

# Nginx component setting: redirect logger to container's std in/out which can be checkeout out via command docker logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# Sync app
RUN mkdir -p /app/backend /app/frontend
COPY ./frontend/dist/ /app/frontend/
COPY ./backend/ /app/backend/
COPY ./docker/pip-requirements.txt /app/backend
COPY ./docker/dict-entrypoint.sh /usr/local/bin
COPY ./docker/dict.conf /etc/nginx/sites-available/default

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
