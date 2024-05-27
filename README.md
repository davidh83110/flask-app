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
```sh
 docker build -t flask-app .
```
```sh
docker run -p 3000:3000 -it -e REDIS_HOST='192.168.68.112' flask-app

```

## Development
---
### Run under Pipenv Shell  
```bash
pipenv shell
python3 main.py
```

### Install PYPI packages with Pipenv
```bash
pipenv install flask ...
pipenv update
```

