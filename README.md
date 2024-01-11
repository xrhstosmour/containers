# containers

This repository contains Docker Compose setups for a variety of applications, encompassing general, development, and deployment environments.

🚧 **Important**: The project is currently under development.

---

**Initial Setup**:

Start by creating a Docker network with the following command:

```bash
docker network create internal
```

---

**Configuration Files**:

Identify files with the 'template.' prefix in the desired container folders. Eliminate this prefix from each of these files and proceed to make any required adjustments.

---

**Launching Containers**:

To use the containers, navigate to their respective directories containing the `docker-compose.yml` file. Run the following command to start the containers:

```bash
docker-compose up -d
```
