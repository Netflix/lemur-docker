Lemur Docker
============

This project is not actively updated and is currently in maintenance mode.

For full documentation, please see the [docs](https://lemur.readthedocs.org).

This repo utilizes docker compose to launch a cluster of containers to support the Lemur project.  This is only meant to be used to **play**.  See the [Issues](#Issues) section for information regarding productionalizing these containers.

----------

Requirements
------------

-   Latest version of [Docker Toolbox](https://www.docker.com/toolbox)
-   Terminal with all docker env variables set

Starting
--------

Start the containers

> docker-compose up

Get the ip to connect to

> docker-machine ip lemur

Stopping
--------

> docker-compose stop

Try It Out
----------

Launch web browser and connect to your docker container's IP over https. 
The default credientials are `lemur/password`

Architecture
-------------

This project launches three containers:

1.  postgres:latest
2.  lemur-nginx:0.2.0
3.  lemur-web:0.2.0

Externally, only lemur-nginx exposes any ports. This container exposes TCP 80 and 443.

The lemur-web container can be altered by the following env vars:

-   `LEMUR_VERSION` (default value: `master`)
    Which branch / tag to build
-   `LEMUR_TARGET` (default version: `develop`)
    Which target to build.
    Recommended values are
    -   `develop`
    -   `release`

Please note that as of Lemur 0.5 python2.7 is no longer supported. See the [Changelog](http://lemur.readthedocs.io/en/latest/changelog.html#id1) for details.

Issues
------

### Default credentials on the web UI

The username for the Lemur web UI is `lemur` and the default password is `password`. You may create new users and disable this service account after the apps has been launched.  

### Default Config

This comes with a default `lemur.conf.py` located under the [`web/`](web/) dir of this repository.
Things like encryption keys and tokens have been filled in these **should** be changed for anything other than experimentation.

There are 2 recommended ways of updating these settings:

1.  Mounting your own settings
    
    In [`docker-compose.yml`](docker-compose.yml), add a line like `<path/to/lemur.conf.py>:/usr/local/src/lemur/lemur.conf.py` under `lemur-web.volumes`
    where `<path/to/lemur.conf.py>` is the path to your custom `lemur.conf.py` file.
    
    Then you simply restart the containers:
    
        docker-compose start
    
2.  Rebuilding image with new settings
    
    Update the file [`web/lemur.conf.py`](web/lemur.conf.py), and rebuild your image files:
    
        docker-compose build lemur-web
    
    Then execute:
    
        docker-compose stop
    
    and
    
    > docker-compose up

Your changes should now be reflected in Lemur.

### Default credentials on the postgres database

The username for the postgres database is `lemur`.  The password for this database is actually set in the api-start.sh file found within the lemur-web container.  This password is set to `lemur`.
