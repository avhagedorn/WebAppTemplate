#!/bin/bash

docker-compose -f docker-compose.yml -p alpha-tracker-app up -d --build --force-recreate
