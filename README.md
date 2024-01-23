# Delivery Fee Calculator API

## Getting Started

### Prerequisites

- Python 3.12
- Docker
- Docker Compose
- Make

### Installing

1. Clone the repository:

```
git clone https://github.com/rhiskk/delivery-fee-calculator.git
```

2. Navigate to the project directory:

```
cd delivery-fee-calculator
```

3. Initialize the virtual environment and install the required packages:

```
make init-venv
```

### Running the Application

To run the application, use the following command:
make run

The application will start running at `http://localhost:8000`.

### API Documentation

To view the API documentation, navigate to `http://localhost:8000/docs` while the application is running.

### Running the Tests

To run the tests, use the following command:
make test

To run the tests and watch for changes, use the following command:
make test-watch

To run the tests with coverage, use the following command:
make test-coverage

### Type Checking

To perform type checking on the code, use the following command:
make type-check

### Cleaning Up

To remove the virtual environment and clean up the project, use the following command:
make clean-venv
