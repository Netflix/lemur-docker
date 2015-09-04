Lemur ZeroToDocker
==================


For full documentation, please see the [wiki](https://lemur.readthedocs.org).

This repo utilizes docker compose to launch a cluster of containers to support the Lemur project.  This is only meant to be used to **play**.  See the [Issues](#Issues) section for information regarding productionalizing these containers.

----------

###Requirements
* Latest version of [Docker Toolbox](https://www.docker.com/toolbox)
* Running boot2docker vm
* Terminal with all docker env variables set

Starting
-------------
First determine the ip address of your boot2docker vm

> boot2docker ip

Replace the host variable in `docker-compose.yaml` with that IP

```
    host: <YOUR IP ADDRESS HERE>
```

Start the conatiners

> docker-compose up

Stopping
-------------
> docker-compose stop

Try It Out
-------------
Launch web browser and connect to your docker container's IP over http. 
The default credientials are `admin/password`


Architecture
-------------

This project launches three containers:

 1. postgres:latest
 2. lemur-nginx:0.2.0
 3. lemur-web:0.2.0

Externally, only lemur-nginx exposes any ports.  This container only exposes TCP 80.  See the [Issues](#Issues) section for an explanation of why TCP 443 was not exposed.


Issues
-------------


----------

**Default credentials on the web UI**
The username for the Lemur web UI is `admin`.  The docker-compose.yml defines the password as `password` by setting the `DOCKER_ADMIN_PASS` environment variable.  

For production use, you will want to modify or remove this default account.

**Default Secrets**
The docker-compose.yml defines a `secret_key` environment variable which are passed into the Flask application.

For production use, you will want to modify these values.

**Default credentials on the postgres database**
The username for the postgres database is `postgres`.  The password for this database is actually set in the api-start.sh file found within the lemur-web container.  This password is set to `password`.

You may wish to change this password for production use.


