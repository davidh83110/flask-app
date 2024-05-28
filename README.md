# Flask Application
This is a Flak RESTfulAPI. Please run the application and vivsit `/swagger` for API documentations.
- [http://localhost:3000](http://localhost:3000)

### Table of Content
- [How to Run](#How-to-Run)
  + [Prerequisites](#prerequisites)
  + [Setup Environment](#setup-environment)
  + [Start Flask Application](#start-flask-application)
    + [In Gunicorn without Docker](#in-gunicorn-without-docker)
    + [In Gunicorn with Docker](#in-gunicorn-with-docker)
    + [Running in local with Kind and Helm Chart](#running-in-local-with-kind-and-helm-chart)
  + [Check Result](#check-result)
- [Development](#development)

## How to Run
This Page will only focus on Flask application, 
if you need any information about `Helm` or run in `Kubernetes`, 
please visit [deploy/README.md](deploy%2FREADME.md).

### Prerequisites
- Python >= 3.10
- Pipenv
- Docker 

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

