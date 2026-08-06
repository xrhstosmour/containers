storage "file" {
  path = "/vault/file"
}

# Port is hardcoded because Vault's HCL config does not reliably support
# environment variable interpolation. If you change it, update the container
# side of the port mapping in `docker-compose.yml` to match.
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
}

ui = true
