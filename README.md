Lemur ZeroToDocker
==================


For full documentation, please see the [docs](https://lemur.readthedocs.org).

This repo utilizes docker compose to launch a cluster of containers to support the Lemur project.  This is only meant to be used to **play**.  See the [Issues](#Issues) section for information regarding productionalizing these containers.

----------

###Requirements
* Latest version of [Docker Toolbox](https://www.docker.com/toolbox)
* Terminal with all docker env variables set

Starting
--------

Create a virtualbox vm *only needed for OS X

> docker-machine create --driver virtualbox lemur

Determine the environment

> docker-machine env lemur

Export the environment to bash

> eval "$(docker-machine env lemur)"

Start the conatiners

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

 1. postgres:latest
 2. lemur-nginx:0.2.0
 3. lemur-web:0.2.0

Externally, only lemur-nginx exposes any ports.  This container only exposes TCP 80.  See the [Issues](#Issues) section for an explanation of why TCP 443 was not exposed.


Issues
------


**Default credentials on the web UI**
The username for the Lemur web UI is `lemur` and the default password is `password`. You may create new users and disable this service account after the apps has been launched.  

**Default Config**
This comes with a default lemur.conf.py located under the /web. Things like encryption keys and tokens have been filled in these **should** be changed for anything other than experimentation. 
If you change a default settings or want to alter the configuration at all you must run the following to rebuild the web docker.

> docker-compose build lemur-web

Then execute:

> docker-compose stop

and

> docker-compose up 

Your changes should now be reflected in Lemur.

**Default credentials on the postgres database**
The username for the postgres database is `lemur`.  The password for this database is actually set in the api-start.sh file found within the lemur-web container.  This password is set to `lemur`.
