import os
import logging
import json
import boto3
import dlt
from dlt.sources.rest_api import rest_api_source

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS Secrets Manager client
secrets_manager = boto3.client('secretsmanager')

def get_secret(secret_name):
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {str(e)}")
        raise

def create_source(api_config):
    return rest_api_source({
        "client": {
            "base_url": api_config['api_base_url'],
            "auth": {
                "token": api_config['api_token'],
            },
            "paginator": {
                "type": "json_response",
                "next_url_path": "paging.next",
            },
        },
        "resources": ["posts", "comments"],
    })

def create_pipeline(db_config):
    return dlt.pipeline(
        pipeline_name="rest_api_example",
        destination='postgres',
        dataset_name="rest_api_data",
        credentials={
            'host': db_config['host'],
            'port': db_config['port'],
            'database': db_config['database'],
            'user': db_config['username'],
            'password': db_config['password'],
        }
    )

def lambda_handler(event, context):
    try:
        # Get secrets
        db_config = get_secret(os.environ['DATABASE_CREDENTIALS_SECRET_ARN'])
        api_config = get_secret(os.environ['API_CREDENTIALS_SECRET_ARN'])

        # Create source and pipeline
        source = create_source(api_config)
        pipeline = create_pipeline(db_config)

        # Run pipeline
        load_info = pipeline.run(source)
        logger.info(f"Load info: {load_info}")

        return {
            'statusCode': 200,
            'body': 'ETL process completed successfully'
        }
    except Exception as e:
        logger.error(f"Error in ETL process: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error in ETL process: {str(e)}'
        }