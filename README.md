# TronPulse Application

TronPulse is a FastAPI-based application for interacting with the Tron blockchain network. This document provides instructions for setting up and running the project.

## Prerequisites

Before proceeding with the setup, ensure you have the following:

- Docker installed on your system
- A properly configured `.env` file with required environment variables

## Setup Instructions

### 1. Configure Environment Variables

Create a `.env` file in the project's root directory and populate it with the necessary environment variables:

# Env type

__ENV__=local

# Database Configuration

POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=your_db_host
POSTGRES_PORT=your_db_port
POSTGRES_DB=your_db_name

# Application Configuration

APP_HOST=0.0.0.0
APP_PORT=8080
DEBUG=True
RELOAD=True

Replace the placeholders (your_db_user, your_db_password, etc.) with your actual database credentials. 2. Build the Docker Image
Navigate to the root directory of the project and build the Docker image:\

docker build -t tronpulse-app .

3. Run the Docker Container
   After building the image, run the container and map port 8080 on your host to port 8080 in the container:

docker run -p 8080:8080 --env-file .env tronpulse-app

4. Access the Application
   Once the container is running, the application will be accessible at:

http://localhost:8080/api/v1/docs

Additional Notes
Ensure that your database is running and accessible with the credentials provided in the .env file.
If you need to change the port, update the APP_PORT variable in the .env file and the -p flag in the docker run command.

Example .env File
Here’s an example of a complete .env file:

# Env type

__ENV__=local

# Database Configuration

POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=tronpulse

# Application Configuration

APP_HOST=0.0.0.0
APP_PORT=8080
DEBUG=True
RELOAD=True

Troubleshooting
Docker Build Fails: Ensure all dependencies are listed in requirements-docs.txt.
Application Fails to Start: Check the logs for errors related to database connectivity or missing environment variables.
This README.md provides clear instructions for setting up the project, configuring the .env file, building the Docker image, and running the application. Let me know if you need further adjustments!
