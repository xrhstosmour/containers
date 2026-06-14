#!/bin/sh
# Creates the default MinIO bucket on first startup.
# Runs as a one-shot job after the MinIO container is healthy.

set -e

MC_HOST="http://${MINIO_ROOT_USER}:${MINIO_ROOT_PASSWORD}@localhost:${MINIO_API_PORT}"
mc alias set local "${MC_HOST}" || true
mc mb "local/${MINIO_DEFAULT_BUCKET}" --ignore-existing || true
mc anonymous set download "local/${MINIO_DEFAULT_BUCKET}" || true
