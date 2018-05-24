# Terra service package

Provides usefull data for terra projects.

## Requirements

On Ubuntu, do not use the system packages, which are too old.
* **docker-ce**: https://docs.docker.com/install/linux/docker-ce/ubuntu/
* **docker-compose**: `sudo pip3 install docker-compose`

## Install

Create a docker.env file and edit the django settings

```bash
cp docker.env.dist docker.env
cp src/project/settings/local.py.dist src/project/settings/local.py
```

Add `ALLOWED_HOSTS = ['*']` in local settings.

After setted the django settings and docker.env, to run with docker, just type :
```bash
$ docker-compose up
```

### Applying Django migrations

```
docker-compose run --rm django /code/venv/bin/python3.6 ./manage.py migrate
```

### Create superuser

```
docker-compose run --rm django /code/venv/bin/python3.6 ./manage.py createsuperuser
```

### Generate API Token

## Usage

After setted the netrc and docker.env, to run with docker, just type :
```bash
$ docker-compose start
```
