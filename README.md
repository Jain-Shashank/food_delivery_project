# Food Delivery System

This is a simple food delivery system implemented in Docker. Follow the instructions below to build, run, and access various endpoints.

### Build Docker Image

Use the following command to build the Docker image:

```bash
docker build -t food_delivery .
```

### Run the Docker container with the following command:

```bash
docker run -p 8000:8000 food_delivery
```

## API Endpoints
## Get Users Details
To retrieve users' details, make a GET request to:
```
http://0.0.0.0:8000/food-delivery/user-details/
```
## Get Monthly Status Details
## To retrieve monthly status details, make a GET request to:
```
http://localhost:8000/food-delivery/monthly-status/?start_month=11&end_month=11
```

Replace start_month and end_month parameters with the desired month range.

Make sure the Docker container is running before making requests to the endpoints.