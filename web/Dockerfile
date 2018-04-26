# Copyright 2014 Netflix, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04
LABEL maintainer="Netflix Open Source Development <talent@netflix.com>"

RUN apt-get update && \
  apt-get install -y curl git build-essential sudo \
    python3 python3-pip python3-dev \
    nodejs npm \
    postgresql postgresql-contrib \
    libpq-dev libssl-dev libffi-dev libsasl2-dev libldap2-dev && \
  update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
  update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
  update-alternatives --install /usr/bin/node node /usr/bin/nodejs 1 && \
  apt-get clean -y && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN locale-gen en_US.UTF-8

ENV LC_ALL=en_US.UTF-8

ENV LEMUR_VERSION=master LEMUR_TARGET=develop

# Install Lemur
RUN git config --global url."https://".insteadOf git:// &&\
  cd /usr/local/src &&\
  git clone https://github.com/netflix/lemur.git &&\
  cd lemur &&\
  git checkout ${LEMUR_VERSION} &&\
  pip install --upgrade pip virtualenv &&\
  export PATH=/usr/local/src/lemur/venv/bin:${PATH} &&\
  virtualenv -p python3 venv &&\
  . venv/bin/activate &&\
  make ${LEMUR_TARGET}

WORKDIR /usr/local/src/lemur

# Create static files
RUN npm install --unsafe-perm && node_modules/.bin/gulp build && \
  node_modules/.bin/gulp package && \
  rm -r bower_components node_modules

ADD lemur.conf.py /usr/local/src/lemur/lemur.conf.py
ADD api-start.sh /usr/local/src/lemur/scripts/api-start.sh
RUN chmod +x /usr/local/src/lemur/scripts/api-start.sh

CMD ["/usr/local/src/lemur/scripts/api-start.sh"]
