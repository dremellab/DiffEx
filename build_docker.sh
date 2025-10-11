#!/bin/bash

commit_id=$1
docker buildx build --platform linux/amd64 \
 --build-arg DIFFEX_COMMIT=${commit_id} \
 -t seqinfomics/diffex:0.5.1-dev -f Dockerfile .  --no-cache > build.log 2>&1 &
echo "Run: tail -f build.log"
