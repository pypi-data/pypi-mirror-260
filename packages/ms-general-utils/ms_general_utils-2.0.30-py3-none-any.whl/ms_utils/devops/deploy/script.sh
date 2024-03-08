#!/bin/bash

set -x
ENV=$1
IMAGE=$2

docker rmi --force "${IMAGE}" || true

docker compose --env-file ./deploy/dockerenv/$ENV.env build --no-cache

docker compose --env-file ./deploy/dockerenv/$ENV.env push
