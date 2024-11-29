import json
import logging
from datetime import datetime
from img_upload import ImageUploader
from db_handler import MetadataHandler
from fetch_userid import JwtDecoderForUserId

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class LambdaHandler:
    def __init__(self):
        self.rds_manager = MetadataHandler()
        self.s3_manager = ImageUploader()
        self.jwt_decoder = JwtDecoderForUserId()  
        pass

    def lambda_handler(self, event, context):
        try:
           
            # If the HTTP method is GET and path is /images/fetch, fetch image metadata
            if event['httpMethod'] == 'GET' and event['path'] == '/images/fetch':
                # Retrieve query parameters if needed
                query_params = event.get('queryStringParameters', {})
                user_id = query_params.get('user_id', None)
                metadata_list = self.rds_manager.fetch_metadata_by_user(user_id)

                return {
                        'statusCode': 200,
                        'body': json.dumps(metadata_list)
                    }
            
            # Decode JWT token and get user ID
            user_id_from_tkn = self.jwt_decoder.decode_token(event)
            logger.info(f"Decoded user ID: {user_id_from_tkn}")

            # Handle file upload to S3
            body = event.get('body')
            file_name = f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            s3_url = self.s3_manager.upload_img_to_s3(body)  

            # Handle metadata upload to RDS

            # Check and create database and table if not exists
            self.rds_manager.check_and_create_database()
            self.rds_manager.check_and_create_table()   
            
            # Get current timestamp for the upload
            upload_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert metadata into RDS
            image_id = f"{user_id_from_tkn}_{file_name}"  # Image ID could be unique based on user_id_from_tkn and file name
            self.rds_manager.insert_metadata(user_id_from_tkn, image_id, file_name, upload_timestamp, s3_url)

            return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Image uploaded successfully',
                        "user_id": user_id_from_tkn,
                        'image_id': image_id,
                        's3_url': s3_url
                    })
                }

        except Exception as e:
                logger.error(f"Error handling Lambda event: {str(e)}")
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': str(e)})
                } 
        pass