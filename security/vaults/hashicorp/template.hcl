storage "file" {
  path = "/vault/file"
}

# Port is hardcoded because Vault's HCL config does not reliably support
# environment variable interpolation. If you change it, update the container
# side of the port mapping in `docker-compose.yml` to match.
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 0
  # Copy `certificates/template.certificate.crt` and `template.private_key.key`
  # to `certificate.crt` and `private_key.key` with real cert/key material.
  # Vault loads the real files below, not the `template.*` placeholders.
  tls_cert_file = "/vault/certificates/certificate.crt"
  tls_key_file = "/vault/certificates/private_key.key"
}

ui = true
