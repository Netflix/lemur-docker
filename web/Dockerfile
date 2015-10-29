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

RUN apt-get update && apt-get install -y curl && curl -sL https://deb.nodesource.com/setup_0.12 | bash - && apt-get -y -q install software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3 && apt-get install -y curl python-dev python-pip git sudo && apt-get -y -q install python-psycopg2 libpq-dev libffi-dev nodejs


# Install Lemur
RUN cd /usr/local/src &&\
  git clone https://github.com/netflix/lemur.git &&\
  cd lemur &&\
  git fetch &&\
  git checkout 0.1.5 &&\
  python setup.py develop

# Create static files
RUN cd /usr/local/src/lemur && npm install --unsafe-perm && node_modules/.bin/gulp build && node_modules/.bin/gulp package && rm -r bower_components node_modules

ADD lemur.conf.py /usr/local/src/lemur/lemur.conf.py 
ADD api-start.sh /usr/local/src/lemur/scripts/api-start.sh
RUN chmod +x /usr/local/src/lemur/scripts/api-start.sh

CMD ["/usr/local/src/lemur/scripts/api-start.sh"]
