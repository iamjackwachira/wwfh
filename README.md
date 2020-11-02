[![Build Status](https://travis-ci.com/iamjackwachira/wwfh.svg?branch=main)](https://travis-ci.com/iamjackwachira/wwfh)
# We Work From Home
Python/Django Clone for https://weworkremotely.com/


## Run locally via Docker

Build first the images and run the webserver on port 8080:

```shell
$ docker-compose up --build # --no-cache to force deps installation
```

To run the tests:

```shell
$ docker-compose run --entrypoint '/usr/bin/env' --rm wwfh_web python3 manage.py test # --keepdb to run faster
```

To run bash:

```shell
$ docker-compose run --entrypoint '/usr/bin/env' --rm wwfh_web bash
```

or if you initialized already a container:

```shell
$ docker exec -it wwfh_web bash
```

To connect to the database when the container is running:

```shell
$ docker exec -it wwfh_postgres psql -U root postgres
```
