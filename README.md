# Delivery Fee Calculator API

### Prerequisites

- Make
- Docker
- Docker Compose
- Python 3.12 (for intellisense)

### IntelliSense

Run `make init-venv` to create a virtual environment and install the necessary Python packages. This step is for IntelliSense features in your IDE. This is not required to run or test the application.

---

The following make targets use `docker-compose` to run the application and commands in a Docker container and thus require the Docker daemon to be running:

## Running the Application

- Run `make run-dev` to start the application in development mode.

The API will be available at [`http://localhost:8000/calculate_delivery_fee`](http://localhost:8000/calculate_delivery_fee).

## Running the Tests

- Run `make test` to run the tests.
- Run `make test-watch` to run the tests in watch mode.
- Run `make test-coverage` to generate a test coverage report.

## Formatting, Linting and Type Checking

- Run `make format` to format the code.
- Run `make lint` to check the code for linting errors.
- Run `make lint-fix` to automatically fix linting errors.
- Run `make type-check` to check the code for type errors.

## OpenAPI Documentation

- Run `make docs` to open the openAPI documentation in your web browser (macOS and Linux only).

If you are using Windows, you can open [`http://localhost:8000/docs`](http://localhost:8000/docs) in your web browser while the app is running.

## Cleaning Up

When you are done using the application, you should clean up the Docker environment:

- Run `make clean-docker` to remove the Docker image for the delivery fee calculator API.

- Run `make clean-all` to remove the Docker image, the virtual environment and the generated coverage report.
