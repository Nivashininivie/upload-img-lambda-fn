import boto3
import os
import base64
from datetime import datetime

class ImageUploader:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = os.environ['BUCKET_NAME']

    def upload_img_to_s3(self, body):

        # Decode base64 if needed
        if isinstance(body, str):
            padding = len(body) % 4
            if padding != 0:
                body += "=" * (4 - padding)
            data = base64.b64decode(body)
        else:
            data = body

        # Generate file name and upload
        file_name = f"upload_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        s3_response = self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=data)
        s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"

        return s3_url
