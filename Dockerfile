FROM python:3.8-slim
MAINTAINER danifr <daferoes gmail com>

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# pandoc intallation from tarball
# copied from https://github.com/dcycle/docker-md2html/blob/master/Dockerfile#L12
RUN apt-get update && \
  apt-get -y --no-install-recommends install curl wget ca-certificates && \
  rm -rf /var/lib/apt/lists/*

RUN curl -L -O $(curl https://api.github.com/repos/jgm/pandoc/releases/latest \
  | grep browser_download_url \
  | grep linux-amd64 \
  | cut -d '"' -f 4)

RUN tar xvf pandoc-*.tar.gz --strip-components 1 -C /usr/local


COPY get_keycloak_docs.py ./
VOLUME /output

CMD [ "python3", "get_keycloak_docs.py", "-v", "--output", "/output/keycloak_docs.epub" ]
