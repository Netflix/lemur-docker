Lemur Docker
============

For full documentation on Lemur, please see the [docs](https://lemur.readthedocs.org).

This repo utilizes docker compose to launch a cluster of containers to support development of the Lemur project. This is only meant for development and testing, not for production. See the [Issues](#Issues) section for information regarding productionalizing these containers.

This project builds the _current state_ of a checked out lemur repository subdirectory, meaning you may make changes and rebuild your container to pick them up. It also has the ability to dump and load another database, in case you want to test with a copy of a real Lemur DB. Alternatively, it has the option to initialize an empty database. Celery tasks will also run, if you choose to enable them.


Requirements
------------

- Latest version of [Docker Engine](https://docs.docker.com/engine/install/) - minimum version 20
- Latest version of [Docker Compose](https://docs.docker.com/compose/install/) - minimum version 1.27

Starting
--------

Check out the lemur-docker and lemur repos:

    git clone git@github.com:Netflix/lemur-docker.git
    cd lemur-docker
    git clone git@github.com:Netflix/lemur.git

Start the containers:

    docker-compose up

Stopping
--------

    docker-compose stop

Try It Out
----------

Launch web browser and connect to your docker container at https://localhost:447. The default credentials are `lemur/admin`.

Architecture
-------------

This project launches three containers:

1. postgres
2. redis
2. lemur

Externally, only `lemur` exposes any ports. This container exposes TCP 87 and 447. We use standard ports to avoid conflicts.

The `lemur` container is built on a local copy of the Lemur code. It runs three processes via `supervisord`:

- nginx
- lemur
- lemur-celery

The file `entrypoint` is used to perform setup and initialization both for postgres and lemur within the `lemur` container.

Note that then `lemur` subdirectory is git ignored, so you may make changes to the lemur repository without causing any changes to show up in `lemur-docker`.

Configuration
-------------

*Lemur configuration*
Lemur configuration can happen in two places:
 - `lemur-env` can be used for a few basic configuration overrides
 - `lemur.conf.py` must be used for any configuration that requires Python execution, and any options not available in `lemur-env`

Note that by defauly, the Celery process is running, but all Celery tasks are disabled. If you wish to enable a Celery task, it should be done in `lemur.conf.py`.

`lemur.conf.py` is mounted on the container, so all you need to do to update these settings is to make the desired changes and restart the containers:
    
        docker-compose stop
        docker-compose start

Your changes should now be reflected in Lemur.

*Database configuration*
This Docker configuration includes three ways to run the database, controlled via the option `POSTGRES_DB_MODE` in `pgsql-env`:
- `init` will create a brand new Lemur database, initialized with base data
- `load-frum-dump` will use specified DB info to dump another database and load it into the container database (see `pgsql-env` for config options)
- blank/not set will reuse whatever data already exists in the volume `lemur-docker_pg_data`

Note that the `init` and `load-from-dump` options will drop whatever data is already in the volume. Aside from those, explicitly deleting the Docker volume will also delete all data. Otherwise, the volume is persistent and should contain persistent data across multiple runs of the Docker container.

Issues
------

### Default credentials on the web UI

The username for the Lemur web UI is `lemur` and the default password is `admin` (unless overriden by environment variable `LEMUR_ADMIN_PASSWORD`). You may create new users and disable this service account after the apps has been launched.  

### Default Config

This comes with a default `lemur.conf.py`.
Things like encryption keys and tokens have been randomized in these **should** be generated and persisted securely for anything other than experimentation.

### Default credentials on the postgres database

The username for the postgres database is `lemur` and the default password is `12345` (located in `pgsql-env`).

### Untrusted web certificate

The certificate used by nginx to serve Lemur in the container is self-signed and untrusted. You would need to use a trusted certificate if you were to run this for anything other than experimentation.