FROM ubuntu:18.04
LABEL maintainer="Netflix Open Source Development <talent@netflix.com>"

ARG DEBIAN_FRONTEND=noninteractive
ARG VERSION

ARG URLCONTEXT

ENV uid 1337
ENV gid 1337
ENV user lemur
ENV group lemur

COPY lemur/ /opt/lemur

RUN addgroup --gid ${gid} ${group} && \
    adduser --gecos "" --disabled-password --ingroup ${group} --uid ${uid} ${user} && \
    apt-get update && \
    apt-get install -y libpq-dev python-dev python3-dev libffi-dev libsasl2-dev libldap2-dev haveged supervisor curl && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs build-essential postgresql nginx git && \
    mkdir -p /opt/lemur /home/lemur/.lemur/ && \
    apt-get install -y python3-pip && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade setuptools && \
    mkdir -p /run/nginx/ /etc/nginx/ssl/ && \
    touch /home/lemur/.lemur/lemur.log && \
    chown -R $user:$group /opt/lemur/ /home/lemur/.lemur/ && \
    chmod o+w /home/lemur/.lemur/lemur.log

RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
    
WORKDIR /opt/lemur

RUN npm install --unsafe-perm && \
    python3 -m pip install -e . && \
    node_modules/.bin/gulp --cwd /opt/lemur build && \
    node_modules/.bin/gulp --cwd /opt/lemur package

COPY entrypoint /
#COPY lemur.conf.py /home/lemur/.lemur/lemur.conf.py
COPY supervisor.conf /
COPY nginx/default.conf /etc/nginx/conf.d/
COPY nginx/default-ssl.conf /etc/nginx/conf.d/

RUN chmod +x /entrypoint
WORKDIR /

HEALTHCHECK --interval=12s --timeout=12s --start-period=30s \  
 CMD curl --fail http://localhost:80/api/1/healthcheck | grep -q ok || exit 1

USER root

ENTRYPOINT ["/entrypoint"]

CMD ["/usr/bin/supervisord","-c","/supervisor.conf"]
