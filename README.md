# Fair Split API

A Django-based API for fair expense splitting in groups. Manage groups, add members, register expenses, and calculate balances between users.

---

## Table of Contents

- [Main Technologies](#main-technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database and Migrations](#database-and-migrations)
- [Running the Server](#running-the-server)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Useful Commands](#useful-commands)
- [Using Just](#using-just)
- [Contributing](#contributing)
- [License](#license)

---

## Main Technologies

- Python 3.13+
- Django 5+
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

---

## Prerequisites

- Python 3.13 or higher
- pip
- Docker and Docker Compose (optional, recommended for development)
- PostgreSQL (if not using Docker)
- [just](https://github.com/casey/just) (optional, for command shortcuts)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <REPO_URL>
   cd fair-split-api
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. Copy the example environment settings file (if it exists) or create a new one:
   ```bash
   cp core/settings/local.py.example core/settings/local.py
   ```
2. Adjust the required environment variables (DB, DEBUG, SECRET_KEY, etc.) in `core/settings/local.py`.

---

## Database and Migrations

1. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

2. **(Optional) Create a superuser for the admin site**
   ```bash
   python manage.py createsuperuser
   ```

---

## Running the Server

- **Locally**
  ```bash
  python manage.py runserver
  ```

- **Using Docker**
  ```bash
  docker-compose up --build
  ```

The server will be available at [http://localhost:8000/](http://localhost:8000/).

---

## Running Tests

```bash
python manage.py test
```

---

## Project Structure

- `accounts/` — User management, authentication, and permissions.
- `expenses/` — Logic for groups, members, and expenses.
- `core/settings/` — Project configuration.
- `core/utils/` — Shared utilities and mixins.
- `requirements.txt` — Project dependencies.
- `docker-compose.yml`, `Dockerfile` — Docker configuration.

---

## Useful Commands

- `python manage.py makemigrations` — Create new migrations.
- `python manage.py migrate` — Apply migrations.
- `python manage.py createsuperuser` — Create an admin user.
- `python manage.py test` — Run tests.
- `python manage.py shell` — Open Django's interactive shell.

---

## Using Just

If you have [just](https://github.com/casey/just) installed, you can use the following shortcuts for common development tasks:

- `just up` — Start the API and database (development environment)
- `just down` — Stop all services
- `just test` — Run tests in the dockerized environment
- `just migrate` — Apply Django migrations
- `just shell` — Open a Django shell
- `just createsuperuser` — Create a Django superuser
- `just logs` — Show API logs

To see all available commands, run:
```bash
just --list
```

---

## Contributing

1. Fork the repository and create a new branch for your feature or fix.
2. Follow Django's coding conventions and best practices.
3. Make sure all tests pass before submitting a PR.
4. Submit your Pull Request and clearly describe your changes.

---

## License

MIT (or as appropriate)