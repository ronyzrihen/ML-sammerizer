#!/bin/bash
# building and deploying the facebook/nllb model using docker
docker build -t translator .
docker run -p 8000:8000 translator


