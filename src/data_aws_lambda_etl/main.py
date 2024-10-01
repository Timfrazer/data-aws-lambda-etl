import os
import logging
import dlt
from dlt.sources.rest_api import rest_api_source

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Get configuration from environment variables
        api_base_url = os.getenv('API_BASE_URL')
        api_token = os.getenv('API_TOKEN')
        pg_host = os.getenv('PG_HOST')
        pg_port = os.getenv('PG_PORT')
        pg_database = os.getenv('PG_DATABASE')
        pg_user = os.getenv('PG_USER')
        pg_password = os.getenv('PG_PASSWORD')

        source = rest_api_source({
            "client": {
                "base_url": api_base_url,
                "auth": {
                    "token": api_token,
                },
                "paginator": {
                    "type": "json_response",
                    "next_url_path": "paging.next",
                },
            },
            "resources": ["posts", "comments"],
        })

        pipeline = dlt.pipeline(
            pipeline_name="rest_api_example",
            destination='postgres',
            dataset_name="rest_api_data",
            credentials={
                'host': pg_host,
                'port': pg_port,
                'database': pg_database,
                'user': pg_user,
                'password': pg_password,
            }
        )

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