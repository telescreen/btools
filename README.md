# btools

A collection of utilities

* RSS: a DIY RSS reader
* Hash: Calculate PBKDF2 Hash (For password generator)


## How to deploy

### Dockerize application

```bash
git clone git@github.com:telescreen/btools.git
cd btools

export DOCKER_HUB_USERNAME=talzeus
docker build -t btools .
docker tag btools ${DOCKER_HUB_USERNAME}/btools:latest
docker push ${DOCKER_HUB_USERNAME}/btools:latest
```

### Deploy on kubernetes cluster

```bash
kubectl create --save-config -f btools-pg.yaml
kubectl create --save-config -f btools.yaml
```

Database need frequent backup. Use the following manual to backup postgresql database

DUMP
// pod-name         name of the postgres pod
// pod-name == postgres-${HASH}

```bash
kubectl exec [pod-name] -- bash -c "pg_dump -U telescreen -d btools" > btools.sql
```

RESTORE
// pod-name         name of the postgres pod
// pod-name == postgres-${HASH}

```bash
cat btools.sql | kubectl exec -i [pod-name] -- psql -U telescreen -d btools
```
