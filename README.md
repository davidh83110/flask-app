# Flask App

## Running in local
```commandline
gunicorn --bind 0.0.0.0 \
              --access-logfile flask-app-gunicorn.log \
              --error-logfile flask-app-gunicron-error.log \
              --log-level debug \
              wsgi:app 

```


## Running in Docker
Build Image
```sh
 export APP_VERSION=0.0.1
 docker build --build-arg APP_VERSION=$APP_VERSION --no-cache -t flask-app .
```

Start Container
```sh
docker run -p 3000:3000 -it -e REDIS_HOST='172.17.0.1' flask-app
```
- `172.17.0.1` is Docker default host network, I am assuming you have a Redis running in Docker.

## Development
### Run under Pipenv Shell  
```bash
pipenv shell
python3 main.py

or 

pipenv python3 main.py
```

### Install PYPI packages with Pipenv
```bash
pipenv install flask ...
pipenv update
```

