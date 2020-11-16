# exponea_task

[![Build Status](https://travis-ci.org/MatejTuray/exponea_task.svg?branch=master)](https://travis-ci.org/MatejTuray/exponea_task)
![CI](https://img.shields.io/badge/Travis-red.svg?style=flat&logo=travis)
[![forthebadge made-with-python](https://img.shields.io/badge/made%20with-python-blue.svg?style=flat-square)](https://www.python.org/)
[![Codecov](https://codecov.io/gh/MatejTuray/exponea_task/branch/master/graph/badge.svg)](https://codecov.io/gh/MatejTuray/exponea_task)

###To start:

```bash
git clone https://github.com/MatejTuray/exponea_task.git
```

```bash
docker-compose up -d
```

###Server settings:

```bash
uvicorn/gunicorn can be modified for a machine/cloud deployment via env variables in docker-compose file such as MAX_WORKERS or WORKERS_PER_CORE
more @ https://github.com/tiangolo/uvicorn-gunicorn-docker#advanced-usage
```

###Docs:

API has 2 docs endpoints, OpenApi - swagger interactive docs and Redoc available at

```json
/api/cdos && /api/cdeor
```
