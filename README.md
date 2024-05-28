# Flask Application
This is a Flak RESTfulAPI. Please run the application and vivsit `/swagger` for API documentations.
- [http://localhost:3000](http://localhost:3000)
- [http://localhost:3000/health](http://localhost:3000/health)
- [http://localhost:3000/metrics](http://localhost:3000)
- [http://localhost:3000](http://localhost:3000)

### Table of Content
- [Data Migration](#data-migration)
- [How to Run](#How-to-Run)
  + [Quick Run](#quick-run)
    + [Docker Compose](#docker-compose)
    + [Kind and Helm Chart](#kind-and-helm-chart)
  + [Prerequisites](#prerequisites)
  + [Setup Environment](#setup-environment)
  + [Start Flask Application](#start-flask-application)
    + [In Gunicorn without Docker](#in-gunicorn-without-docker)
    + [In Gunicorn with Docker](#in-gunicorn-with-docker)
    + [Running in local with Kind and Helm Chart](#running-in-local-with-kind-and-helm-chart)
  + [Check Result](#check-result)
- [Development](#development)

## Data Migration
The `/history` API will require some history data in place so that it can return to user,
so we have [scripts/migrations.py](scripts%2Fmigrations.py) here for helping to inject initial data. 
The script will be executed when we run [scripts/entrypoint.sh](scripts%2Fentrypoint.sh) in Docker environment.

If you are not in Docker environment, please run it manually before start the application.
```commandline
cd scripts
python3 migrations.py
```

## How to Run
This Page will only focus on Flask application, 
if you need any information about `Helm` or run in `Kubernetes`, 
please visit [deploy/README.md](deploy%2FREADME.md).

### Quick Run
#### Docker Compose
```commandline
docker-compose up --build -d
```
- Hardcode the password in the `docker-compose.yaml`, it can also use `docker-compose secret from file`.

#### Kind and Helm Chart
```commandline
cd ./deploy
sh ./startup.sh
```
- More information, please visit [deploy/README.md](deploy%2FREADME.md).

### Prerequisites
- Python >= 3.10
- Pipenv
- Docker 
- Redis Server

### Setup Environment
- Install Pipenv 
  ```commandline
  python -m pip install --upgrade pip
  pip install pipenv --no-cache-dir
  ```
- Install Dependencies
  ```commandline
  pipenv install --system --deploy --ignore-pipfile
  ```
- Start Redis Locally
  ```commandline
   docker run -p 6379:6379 -itd redis:alpine                  
  ```
  
### Start Flask Application
#### In Gunicorn without Docker
```commandline
gunicorn --bind 0.0.0.0:3000 \
            --access-logfile flask-app-gunicorn.log \
            --error-logfile flask-app-gunicron-error.log \
            --log-level debug \
            wsgi:app
```

#### In Gunicorn with Docker
- Build Docker Image
  ```commandline
   export APP_VERSION=0.0.1
   docker build --build-arg APP_VERSION=$APP_VERSION --no-cache -t flask-app .
  ```
- Run Docker Container
  ```commandline
  docker run -p 3000:3000 -it -e REDIS_HOST='172.17.0.1' flask-app
  ```
  - `172.17.0.1` is Docker default host network, I am assuming you have a Redis running in Docker.


#### Running in local with Kind and Helm Chart
please visit [deploy/README.md](deploy%2FREADME.md).
- [Helm Chart Home Page - https://davidh83110.github.io/flask-app](https://davidh83110.github.io/flask-app/)


### Check Result
After the applciation is started, you can always vivist the pages on browser --
[http://localhost:3000](http://localhost:3000) .



## Development
### Run under Pipenv Shell  
```bash
pipenv install --deploy
pipenv shell
python3 main.py
```
or 
```bash
pipenv install --deploy
pipenv run python3 main.py
```

### Install PYPI packages with Pipenv
```bash
pipenv install flask ...
pipenv update
```

### Run Unittest
```commandline
pipenv shell
pytest
```

