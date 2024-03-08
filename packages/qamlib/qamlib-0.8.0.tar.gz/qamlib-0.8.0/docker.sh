#!/usr/bin/env bash
set -eou pipefail

if [[ $# -gt 0 ]];
then
    IMAGE=quay.io/pypa/manylinux_2_28_x86_64
else
    REGISTRY=registry.gitlab.com/qtec/software/images/
    IMAGE=python:slim
    IMAGE=$REGISTRY$IMAGE
fi

docker run --rm -it -v $(pwd):$(pwd) -w$(pwd) -v $(pwd)/.cache:/root/.cache --entrypoint /bin/bash $IMAGE
