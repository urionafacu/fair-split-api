# Justfile for development and testing of the Fair Split API project

# Start the API and database (development environment)
up:
    docker-compose up api db

# Stop all services
down:
    docker-compose down

# Run tests in the dockerized environment
test:
    docker-compose run --rm test

# Apply Django migrations
migrate:
    docker-compose run --rm api python manage.py migrate

# Open a Django shell
shell:
    docker-compose run --rm api python manage.py shell

# Create a Django superuser
createsuperuser:
    docker-compose run --rm api python manage.py createsuperuser

# Show API logs
logs:
    docker-compose logs -f api 