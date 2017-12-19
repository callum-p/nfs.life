#!/bin/sh -e

export SERVICE_NAME=${SERVICE_NAME:-nsf-life}
export STAGE=${STAGE:-dev}
export IMAGE_BUCKET=${IMAGE_BUCKET:-$SERVICE_NAME-$STAGE-images}

sls create_domain --stage $STAGE
sls deploy --stage $STAGE

aws s3 cp images/ s3://${IMAGE_BUCKET}/ --recursive
