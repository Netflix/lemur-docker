#############  BUILDER  #############
FROM ubuntu:20.04 as builder
LABEL maintainer="Netflix Open Source Development <talent@netflix.com>"

ARG DEBIAN_FRONTEND=noninteractive
ARG VERSION

ARG URLCONTEXT

COPY lemur/ /opt/lemur
WORKDIR /opt/lemur

RUN apt-get update && \
    apt-get -y --no-install-recommends upgrade && \
    apt-get install -y --no-install-recommends libpq-dev curl build-essential locales libffi-dev libsasl2-dev libldap2-dev \
        dh-autoreconf git python3-dev python3-pip python3-venv python3-wheel nodejs npm && \
    locale-gen en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && \
    npm config set registry http://registry.npmjs.org/ && \
    npm install npm -g && \
    echo "Running with nodejs:" && node -v && \
    python3 -m venv /opt/venv && \
    echo "Running with python:" && /opt/venv/bin/python3 -c 'import platform; print(platform.python_version())' && \
    /opt/venv/bin/python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    /opt/venv/bin/python3 -m pip install --no-cache-dir -e . && \
    npm install --unsafe-perm && \
    node_modules/.bin/gulp --cwd /opt/lemur build && \
    node_modules/.bin/gulp --cwd /opt/lemur package && \
    npm cache clean --force && \
    rm -rf node_modules && \
    python3 -c 'print(" \033[32m BUILDER DONE \033[0m ")'

#############  APP  #############
FROM ubuntu:20.04
LABEL maintainer="Netflix Open Source Development <talent@netflix.com>"

ARG DEBIAN_FRONTEND=noninteractive
ARG VERSION

ARG URLCONTEXT

ENV uid 1337
ENV gid 1337
ENV user lemur
ENV group lemur

# TODO: do not copy build artefacts
COPY --from=builder /opt/lemur /opt/lemur
COPY --from=builder /opt/venv /opt/venv

WORKDIR /opt/lemur

RUN addgroup --gid ${gid} ${group} && \
    adduser --gecos "" --disabled-password --ingroup ${group} --uid ${uid} ${user} && \
    apt-get update && apt-get -y --no-install-recommends upgrade && \
    apt-get -y --no-install-recommends install python3 locales haveged supervisor curl postgresql-client openssl && \
    locale-gen en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && \
    mkdir -p /opt/lemur /home/lemur/.lemur/ && \
    touch /home/lemur/.lemur/lemur.log && \
    chown -R $user:$group /opt/lemur/ /home/lemur/.lemur/ && \
    chmod o+w /home/lemur/.lemur/lemur.log && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/ && \
    python3 -c 'print(" \033[32m APP BUILD DONE \033[0m ")'

COPY ./files/entrypoint /
#COPY lemur.conf.py /home/lemur/.lemur/lemur.conf.py
COPY ./files/supervisor.conf /

RUN chmod +x /entrypoint
WORKDIR /

HEALTHCHECK --interval=12s --timeout=12s --start-period=30s \
 CMD curl --fail http://localhost:80/api/1/healthcheck | grep -q ok || exit 1

USER root

ENTRYPOINT ["/entrypoint"]

CMD ["/usr/bin/supervisord","-c","/supervisor.conf"]