#!/bin/sh
# Renders the S3 identity file, then hands over to the image's own
# entrypoint.
#
# SeaweedFS reads its S3 credentials from a JSON file and has no way to
# take them from the environment, so the file is written at start from
# the same variables every other service here uses. Writing it to a
# path inside the container rather than into a mounted directory keeps
# the secret off the host disk.

set -e

# The credentials are interpolated into JSON below. A value carrying a
# double quote or a backslash would produce a file SeaweedFS cannot
# parse, and the only symptom is every request answering 403, so it is
# refused here where the reason is obvious. `setup.sh` generates
# URL-safe values that never contain either.
case "${STORAGE_ACCESS_KEY}${STORAGE_SECRET_KEY}" in
  *'"'* | *'\\'*)
    echo "STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY must not contain" \
      "a double quote or a backslash." >&2
    exit 1
    ;;
esac

mkdir -p /etc/seaweedfs

cat > /etc/seaweedfs/s3.json <<JSON
{
  "identities": [
    {
      "name": "application",
      "credentials": [
        {
          "accessKey": "${STORAGE_ACCESS_KEY}",
          "secretKey": "${STORAGE_SECRET_KEY}"
        }
      ],
      "actions": ["Admin", "Read", "Write", "List", "Tagging"]
    }
  ]
}
JSON

# The image's entrypoint drops privileges to the `seaweed` user, so a
# root-owned 0600 file is unreadable by the server that needs it.
chown seaweed:seaweed /etc/seaweedfs/s3.json
chmod 600 /etc/seaweedfs/s3.json

exec /entrypoint.sh "$@"
