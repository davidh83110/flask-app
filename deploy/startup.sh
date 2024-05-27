#!/bin/bash

# Check kind
kind version
if [[ $? -eq 0 ]]; then
  echo "kind found."
else
  echo "kind not found, please try to install by \`brew install kind\` (MacOS)."
  exit 1
fi;

## Create Kind Cluster
kind create cluster --config ./kind-conf.yaml -n kind-flask

## Install Ingress-Nginx
helm install ingress-nginx ingress-nginx/ingress-nginx -f ./ingress-nginx-values.yaml
sleep 3

## Apply secret
kubectl apply -f ./secrets.yaml

## Deploy Redis
helm upgrade -i redis oci://registry-1.docker.io/bitnamicharts/redis -f ./redis-values.yaml
sleep 3

## Deploy Flask
helm upgrade -i flask-app ./charts -f ./flask-app-values.yaml

## Check results
helm list
kubectl get pod


MAX_RETRIES=60
RETRY_COUNT=0
until curl -L -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
      echo "Services are not ready after $MAX_RETRIES retries."
      exit 1
  fi
  echo "Waiting for services to start... (Attempting: $RETRY_COUNT)"
  sleep 3
done

echo "Server is up and running."
curl -L http://localhost:3000
