import json
from lambda_handler import LambdaHandler  

def lambda_handler(event, context):
    try:
        handler = LambdaHandler()
        response = handler.lambda_handler(event, context) 
        return response

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
