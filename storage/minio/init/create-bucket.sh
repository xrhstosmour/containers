#!/bin/sh
# Creates the default MinIO bucket on first startup.
# Runs as a one-shot job after the MinIO container is healthy.

set -e

# URL-encodes a string so it can be safely used in the userinfo part of a URL.
urlencode() {
  string="$1"
  length="${#string}"
  encoded=""
  i=1
  while [ "$i" -le "$length" ]; do
    char=$(printf '%s' "$string" | cut -c"$i")
    case "$char" in
      [a-zA-Z0-9.~_-])
        encoded="${encoded}${char}"
        ;;
      *)
        hex=$(printf '%s' "$char" | od -An -tx1 | tr -d ' \n')
        encoded="${encoded}%$(printf '%s' "$hex" | tr '[:lower:]' '[:upper:]')"
        ;;
    esac
    i=$((i + 1))
  done
  printf '%s' "$encoded"
}

MC_USER=$(urlencode "${MINIO_ROOT_USER}")
MC_PASSWORD=$(urlencode "${MINIO_ROOT_PASSWORD}")
MC_HOST="http://${MC_USER}:${MC_PASSWORD}@minio:${MINIO_API_PORT}"
mc alias set local "${MC_HOST}"
mc mb "local/${MINIO_DEFAULT_BUCKET}" --ignore-existing
mc anonymous set download "local/${MINIO_DEFAULT_BUCKET}"
