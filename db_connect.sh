#!/bin/bash
mongo ${MONGO_SERVER}:${MONGO_PORT}/${MONGO_DB} -u ${MONGO_USER} -p ${MONGO_PASS}

