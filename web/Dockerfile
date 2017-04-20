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

FROM ubuntu:14.04
MAINTAINER Netflix Open Source Development <talent@netflix.com>

RUN apt-get update && \
  apt-get -y install software-properties-common && \
  add-apt-repository -y ppa:jonathonf/python-3.5 

RUN apt-get update && \
  apt-get install -y curl python3.5-dev python3-pip git sudo libpq-dev libffi-dev \
    python3-psycopg2 postgresql-client-9.3 postgresql-contrib-9.3 postgresql-9.3 && \
  update-alternatives --install /usr/bin/python python /usr/bin/python3.5 1 && \

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - && \
  apt-get -y install nodejs && \
  update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN locale-gen en_US.UTF-8 

ENV LC_ALL=en_US.UTF-8


# Install Lemur
RUN git config --global url."https://".insteadOf git:// &&\
  cd /usr/local/src &&\
  git clone https://github.com/netflix/lemur.git &&\
  cd lemur &&\
  git fetch &&\
  pip install --upgrade virtualenv &&\
  virtualenv venv &&\
  export PATH=/usr/local/src/lemur/venv/bin:${PATH} &&\
  pip install --upgrade pip virtualenv &&\
  git checkout 0.5.0 &&\
  make develop

# Create static files
RUN cd /usr/local/src/lemur && npm install --unsafe-perm && node_modules/.bin/gulp build && node_modules/.bin/gulp package && rm -r bower_components node_modules

ADD lemur.conf.py /usr/local/src/lemur/lemur.conf.py 
ADD api-start.sh /usr/local/src/lemur/scripts/api-start.sh
RUN chmod +x /usr/local/src/lemur/scripts/api-start.sh

CMD ["/usr/local/src/lemur/scripts/api-start.sh"]
