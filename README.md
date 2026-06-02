# containers

This repository contains Docker Compose setups for a variety of applications, encompassing general, development, monitoring, and deployment environments.

🚧 **Important**: The project is currently under development.

---

**Table of Contents**:

- Available Services
- Initial Setup
- Configuration Files
- Launching Containers

---

**Available Services**:

- **Databases**
  - PostgreSQL (`databases/postgresql`)
  - Redis (`databases/redis`)
  - pgAdmin4 (`databases/manage/pgadmin4`)
  - Redis Commander (`databases/manage/redis_commander`)
  - Metabase (`databases/manage/metabase`)
- **Distribute**
  - RabbitMQ (`distribute/brokers/rabbitmq`)
  - RedBeat (`distribute/scheduler/redbeat`)
- **Development**
  - Mailpit (`email/mailpit`)
- **Monitoring**
  - GlitchTip (`monitoring/codebase/glitchtip`)
- **Networking**
  - Traefik (`networking/proxies/traefik`)
- **Security**
  - HashiCorp Vault (`security/vaults/hashicorp`)
- **Operating Systems**
  - Windows (`oses/windows`)

---

**Initial Setup**:

Start by creating a Docker network with the following command:

```bash
docker network create internal
```

---

**Configuration Files**:

Identify files with the 'template.' prefix in the desired container folders. Eliminate this prefix from each of these files and proceed to make any required adjustments. Do not forget to edit the files inside the configuration folders, according to your needs.

---

**Launching Containers**:

To use the containers, navigate to their respective directories containing the `docker-compose.yml` file. Run the following command to start the containers:

```bash
docker-compose up -d
```
