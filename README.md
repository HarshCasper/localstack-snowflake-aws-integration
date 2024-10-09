# Connecting LocalStack AWS Emulator to LocalStack Snowflake Emulator

This repository provides a simple proof-of-concept (PoC) demonstrating how to connect the LocalStack AWS emulator to the LocalStack Snowflake emulator. It uses Docker Compose to set up three containers:

1.  **`localstack-snowflake`**: This container runs the Snowflake emulator, which can be accessed via the hostname `snowflake.localhost.localstack.cloud`.
2.  **`localstack-aws`**: This container runs the AWS emulator, accessible via `localhost:4666`.
3.  **`coredns`**: This container uses a custom `Corefile` for DNS configuration. It redirects requests for `snowflake.localhost.localstack.cloud` to the Snowflake container and requests to `amazonaws.com` or `localhost.localstack.cloud` to the LocalStack AWS container.

Additionally, a `run.sh` script is mounted into the `localstack-aws` container, which runs after LocalStack is initialized and ready to serve requests. This script:

1.  Creates an S3 bucket and an EMR cluster.
2.  Retrieves a Python script (`main.py`) that creates a Snowflake table and inserts some data.
3.  Executes the script, demonstrating Snowflake and AWS service integration.

## Prerequisites

-   [LocalStack Auth Token](https://docs.localstack.cloud/getting-started/auth-token/)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [Python 3.10](https://www.python.org/downloads/)
-   [`pip`](https://pip.pypa.io/en/stable/installation/)
-   [`pytest`](https://docs.pytest.org/en/stable/)

## Instructions

Before starting the Docker Compose setup, ensure the `LOCALSTACK_AUTH_TOKEN` is properly set:

```bash
export LOCALSTACK_AUTH_TOKEN=<your-auth-token>
docker-compose up
```

This will pull the required images and launch the LocalStack AWS and Snowflake containers. The `localstack-aws` logs will show EMR cluster provisioning and the execution of the Python script.

Once the containers are running, you can validate the setup by running tests with `pytest`. The tests will:

-   Verify that the `READY` stage script (`run.sh`) completed successfully.
-   Check that the EMR cluster exists and the last step in the cluster was executed.
-   Confirm that the Snowflake table was created and data was inserted correctly.

Run the following command to execute the tests:

```bash
pytest -v --ignore=volume
```

You should see the following output:

```bash
=================================================== test session starts ===================================================
platform darwin -- Python 3.10.14, pytest-8.3.3, pluggy-1.5.0 -- /Users/harshcasper/.pyenv/versions/3.10.14/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/harshcasper/Downloads/snowflake
plugins: anyio-4.4.0
collected 3 items                                                                                                         

tests/test_infra.py::test_emr_cluster PASSED                                                                        [ 33%]
tests/test_infra.py::test_snowflake_connection_and_query PASSED                                                     [ 66%]
tests/test_infra.py::test_localstack_initialization PASSED                                                          [100%]

==================================================== 3 passed in 0.81s ====================================================
```

## How It Works

The `CoreDNS` container is responsible for DNS redirection, which allows us to seamlessly route traffic to the appropriate service container, whether it’s AWS services or the Snowflake emulator.

-   The `localstack-snowflake` container provides the Snowflake functionality, allowing Snowflake-specific queries to be executed within a LocalStack environment.
-   The `localstack-aws` container integrates with LocalStack's EMR and S3 services to demonstrate end-to-end data operations, such as running an EMR cluster and interacting with Snowflake via Python scripts.

The `run.sh` script handles the initial setup, ensuring that resources like S3 buckets and EMR clusters are available, and triggering the execution of the Snowflake operations.

## License

This project is licensed under the Apache 2.0 License.
