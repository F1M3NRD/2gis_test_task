# 2gis_test_task

This is a test task for 2gis team

## Usage in Docker

Clone repository to your local machine:

```
git clone https://github.com/F1M3NRD/2gis_test_task.git
```

Navigate to root directory (2gis_test_task) and build docker image:

```
docker build -t 2gis_test_task .
```

docker run:

```
docker run -it 2gis_test_task
```

## Common usage

Clone repository:

```
git clone https://github.com/F1M3NRD/2gis_test_task.git
```

Requirements:
```
requests
pytest
```

Navigate to root directory (2gis_test_task) and execute:

```
pytest -v src/regions_test.py
```