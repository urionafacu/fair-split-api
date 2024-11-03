#!/bin/bash

# Variables

DOCKER_COMPOSE_FILE="docker-compose.yml"

function check_docker_compose {
  if ! [ -x "$(command -v docker-compose)" ]; then
    echo "Error: docker-compose is not installed"
    exit 1
  fi
}

# Step 1: Check for docker-compose

echo "Checking if docker-compose is installed"
check_docker_compose

# Step 2: Build Docker image and start containers
echo "Building image and starting containers"
docker-compose -f $DOCKER_COMPOSE_FILE up -d --build

# Step 3: Run migrations
echo "Applying Django migrations"
docker-compose exec api python manage.py migrate

# Step 4: (Optional): Create Django superuser if necessary
echo "Do you want to create a superuser? (y/n)"
read create_superuser

if [ "$create_superuser" = "y" ]; then
  docker-compose exec api python manage.py createsuperuser
fi

echo "Server running on http://127.0.0.1:4000"

# Step 5: Follow logs
echo "Following logs from the server. Use Ctrol+C for exit"
docker-compose logs -f api
