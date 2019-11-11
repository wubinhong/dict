FROM ubuntu:18.04
MAINTAINER Binghong wu <wubinhong2012@gmail.com>

# basic flask environment
COPY ./docker/sources.list /etc/apt/
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev curl && rm -rf /var/lib/apt/lists/*
#RUN apt-get install -y build-essential

# sync app
RUN mkdir -p /app
COPY ./docker/requirements.txt /app
COPY ./backend/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000

# health check
HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -fs http://localhost:5000 || exit 1

# startup app
ENTRYPOINT ["python3"]
CMD ["app.py"]