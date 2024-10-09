import pytest
import boto3
import snowflake.connector as sf
import time
import requests

def test_emr_cluster():
    emr_client = boto3.client('emr', endpoint_url='http://localhost:4666')

    # Check for the EMR cluster
    response = emr_client.list_clusters(ClusterStates=['RUNNING', 'WAITING'])
    cluster_id = None
    for cluster in response['Clusters']:
        if cluster['Name'] == 'emr-snowflake-cluster':
            cluster_id = cluster['Id']
            break

    assert cluster_id is not None, "EMR cluster 'emr-snowflake-cluster' not found"

    # Check the steps in the cluster
    steps_response = emr_client.list_steps(ClusterId=cluster_id)
    assert len(steps_response['Steps']) > 0, "No steps found in the EMR cluster"

    # Check if the last step was completed successfully
    last_step = steps_response['Steps'][0]
    assert last_step['Status']['State'] == 'COMPLETED', f"Last step is not completed. Current state: {last_step['Status']['State']}"

def test_snowflake_connection_and_query():
    # Connect to Snowflake
    sf_conn_obj = sf.connect(
        user="test",
        password="test",
        account="test",
        database="test",
        warehouse="test_warehouse",
        role="test_role",
        host="snowflake.localhost.localstack.cloud",
    )
    sf_cur_obj = sf_conn_obj.cursor()

    # Execute query
    sf_cur_obj.execute("SELECT name, skill FROM ability")
    result = sf_cur_obj.fetchall()

    # Assertions on Snowflake query results
    assert len(result) == 3, f"Expected 3 rows, but got {len(result)}"
    assert result[0] == ('John', 'SQL'), f"Expected ('John', 'SQL'), but got {result[0]}"
    assert result[1] == ('Alex', 'Java'), f"Expected ('Alex', 'Java'), but got {result[1]}"

    # Close Snowflake connection
    sf_cur_obj.close()
    sf_conn_obj.close()

def test_localstack_initialization():
    response = requests.get('http://localhost:4666/_localstack/init')
    init_status = response.json()

    ready_script = next((script for script in init_status['scripts'] if script['stage'] == 'READY'), None)
    assert ready_script is not None, "No READY stage script found"
    assert ready_script['state'] == "SUCCESSFUL", f"READY stage script state is {ready_script['state']}, expected SUCCESSFUL"
