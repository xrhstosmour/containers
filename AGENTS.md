# AGENTS.md

Guidance for AI agents working in this repository. See `README.md` for the
human-facing service list and setup steps.

## What this repository is

A collection of independent Docker Compose setups for self-hosted
infrastructure (databases, brokers, monitoring, networking, security). Each
service lives in its own directory with its own `docker-compose.yml`. There is
no root compose file and no `include:` wiring the services together, each
directory is a separate Compose project that a user starts on its own with
`docker compose up -d` from inside that directory.

## Conventions

- **`template.*` files are placeholders, not defaults.** Every `template.env`,
  `template.hcl`, and similar file uses obviously-fake values (`1234`,
  `5678`, `'string_with_special_characters'`) on purpose, so a user can't
  accidentally deploy without consciously replacing every value. Never
  change a placeholder to a real-looking value (a real port number, a
  plausible password) even if it happens to be technically correct, that
  defeats the whole point. When one service's `template.env` needs to
  reference another service's config (see "Cross-project dependencies"
  below), use a placeholder that's visibly different from the original
  file's placeholder for the same concept, so a user can't mistake the copy
  as "already in sync."
- **Required variables use `${VAR?Variable not set}`.** This makes
  `docker compose up` hard-fail instead of silently starting with an empty
  value. Preserve this pattern for any new required variable.
- **Services share one external network named `internal`.** Created once by
  the user (`docker network create internal`), referenced as `external: true`
  in every compose file. Don't introduce `network_mode: host` or a new
  per-service network unless a service genuinely needs isolation.
- **TODO comments at the top of a `docker-compose.yml`** mark known,
  intentionally deferred gaps (e.g. "use Secrets instead of plain env vars").
  Don't silently fix one as a side effect of an unrelated change, and don't
  remove a TODO without actually addressing it.

## Cross-project dependencies

Because each directory is a separate Compose project, `depends_on` cannot
reference a service defined in another directory's `docker-compose.yml`,
Compose will fail with `depends on undefined service`. If a service needs to
wait on another project's container being reachable (e.g. a Postgres client
waiting on `databases/postgresql`), don't use `depends_on` for it. Instead,
wait on the host:port directly in the container's startup command. The
reference implementation is `distribute/scheduler/redbeat/docker-compose.yml`
(uses `wait-for-it.sh`); simpler stock images without a shell script fetched
in usually work fine with a plain `sh`/`bash` TCP wait loop instead (avoid
adding a new external script download to a stock image just for this).

`depends_on` is fine, and should use `condition: service_healthy` where a
real healthcheck exists, when the dependency is on a service defined in the
*same* `docker-compose.yml` file (e.g. `databases/redis`'s
`redis-cluster-init` depending on its own cluster nodes).

## RabbitMQ config templating

`distribute/brokers/rabbitmq/configuration/rabbitmq.conf` is a template, not
read directly by RabbitMQ. Compose only interpolates `${VAR}` inside compose
YAML, never inside bind-mounted files, and RabbitMQ's Cuttlefish config
format does no environment substitution of its own. `render-config.sh`
(mounted into the container, run via the compose `command:` override)
substitutes the file's `$(VAR)` placeholders from the container's real
environment at startup, writes the result to the actual config path, then
execs the official entrypoint. If you add a new tunable to `rabbitmq.conf`
that needs to vary by environment, add it as a `$(VAR)` placeholder there and
wire the corresponding substitution into `render-config.sh`, don't hardcode a
literal value into the template, that value can never actually be changed by
a user editing `.env` alone.

## Validating changes

There's no automated test suite in this repository. Validate changes with:

- `docker compose config` from the service's directory, using a scratch
  `--env-file` populated with dummy values for every `?Variable not set`
  var, to confirm the file is syntactically valid and cross-service
  references (or the lack of them) resolve correctly.
- `bash -n <script>` and `shellcheck <script>` for shell script changes.
- `python3 -m py_compile <file>` for the RedBeat app
  (`distribute/scheduler/redbeat/app/`), the only Python code in this repo.
- A real `docker build`/`docker run` where feasible, especially for anything
  touching an image's entrypoint or command chain, static review alone can
  miss ordering issues (e.g. how an official image's entrypoint re-execs
  itself to drop root privileges).

## Commits and PRs

Follow the user's global commit/PR conventions (imperative, single-topic,
backtick technical identifiers in both commit messages and PR titles, e.g.
`` Fix `RabbitMQ` conf variable substitution ``, not `Fix RabbitMQ conf
variable substitution`). Branch naming in this repo is `fix/<topic>` for
bug fixes and `feature/<topic>` for new capabilities, one topic per branch,
independently mergeable, matching the existing history
(`fix/redis-minimum-size-placeholder`, `fix/postgresql-additional-databases`,
etc). Never invent a `feat:`/`fix:` prefix in a title or commit subject.
