FROM python:3.8.6-slim

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/2gis_test_task/

ENTRYPOINT ["/usr/local/bin/pytest"]

CMD ["-v", "src/regions_test.py"]