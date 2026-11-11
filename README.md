# Hiilipörssi Odoo 20 Community (prototype)

Shared local development setup for the Hiilipörssi Odoo 20 Community prototype.

- Odoo core runs from the official image `odoo:20.0`. We do not clone or fork Odoo core.
- PostgreSQL 16 runs in a container.
- Our custom addons live in `addons/` and are mounted into Odoo at `/mnt/extra-addons`.
- Each developer has their own local database in a Docker volume. Git shares addons, not data.

Production hosting is not chosen yet, and Enterprise is not added yet. This setup is for development only.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS or Windows), running
- Git
- Cursor

## First-time setup

```bash
git clone <repo-url> hp-odoo
cd hp-odoo
docker compose pull
docker compose up -d
```

Then open <http://localhost:8069/web/database/manager> and create a database:

- Database name: `hp`
- Master password: `admin` (the Odoo default; local only)
- Demo data: leave unchecked

## Daily use

```bash
docker compose up -d                 # start
docker compose stop                  # stop, keep data
docker compose logs -f odoo          # follow Odoo logs
docker compose restart odoo          # restart Odoo after installing or updating modules
```

## Creating a custom module

```bash
docker compose run --rm odoo odoo scaffold hp_example /mnt/extra-addons
docker compose run --rm odoo odoo -d hp -i hp_example --stop-after-init
docker compose restart odoo
```

Module names use the `hp_` prefix. Extend core views with inheritance; do not edit core.

After changing XML views or data files, upgrade the module:

```bash
docker compose run --rm odoo odoo -d hp -u hp_example --stop-after-init
docker compose restart odoo
```

Python changes reload automatically in dev mode, but a restart after installing or upgrading is still needed.

## Updating Odoo to the latest Community build

The tag `odoo:20.0` moves with the nightly builds within major version 20:

```bash
docker compose pull
docker compose up -d
```

Then upgrade the custom modules if needed (see above).

## Resetting local data

This deletes all local databases and the filestore. Use it only when you want a clean start:

```bash
docker compose down -v
```

## Git workflow

- `main` always installs and starts.
- Work on a branch named `feature/short-name`.
- Commit locally when a slice installs and upgrades cleanly in your own database.
- Push your branch at least at the end of each working day, and whenever the other person needs to test it.
- Open a pull request into `main`. Do not push directly to `main`.
- Never commit database dumps, the filestore, `.env` files, or Odoo core.

Cursor rules in `.cursor/rules/` describe these conventions for both developers.
