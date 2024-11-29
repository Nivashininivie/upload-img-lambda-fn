import pymysql
import os
from datetime import datetime

class MetadataHandler:

    def __init__(self):
        self.rds_host = os.environ['RDS_HOST']
        self.rds_port = 3306
        self.rds_user = os.environ['RDS_USER']
        self.rds_password = os.environ['RDS_PASSWORD']
        self.rds_db_name = os.environ['RDS_DB_NAME']

    def _connect(self):
        """Helper method to connect to the RDS MySQL database."""
        return pymysql.connect(
            host=self.rds_host,
            port=self.rds_port,
            user=self.rds_user,
            password=self.rds_password,
            database=self.rds_db_name,
            autocommit=True
        )
    
    def insert_metadata(self, user_id, image_id, filename, upload_timestamp, s3_url):
        """Insert image metadata into the RDS table."""
        try:
            connection = self._connect()
            cursor = connection.cursor()

            # Insert metadata into the image_metadata table
            cursor.execute("""
                INSERT INTO image_metadata (user_id, image_id, filename, upload_timestamp, s3_url)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, image_id, filename, upload_timestamp, s3_url))
            print(f"Metadata for image {image_id} inserted into RDS.")
        except Exception as e:
            print(f"Error inserting metadata into RDS: {str(e)}")
            raise
        finally:
            connection.close()

    def fetch_metadata_by_user(self, user_id):
        """Fetch metadata for images uploaded by a specific user."""
        try:
            connection = self._connect()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM image_metadata WHERE user_id = %s", (user_id,))
            results = cursor.fetchall()

            # Convert results to a list of dictionaries and handle datetime serialization
            metadata_list = []
            for row in results:
                metadata_dict = {
                    'user_id': row[0],
                    'image_id': row[1],
                    'filename': row[2],
                    'upload_timestamp': row[3].isoformat() if isinstance(row[3], datetime) else row[3],
                    's3_url': row[4]
                }
                metadata_list.append(metadata_dict)

            return metadata_list
        except Exception as e:
            print(f"Error fetching metadata from RDS: {str(e)}")
            raise
        finally:
            connection.close()
    
    def check_and_create_database(self):
        """Check if the database exists, if not, create it."""
        connection = pymysql.connect(
            host=self.rds_host,
            port=self.rds_port,
            user=self.rds_user,
            password=self.rds_password,
            autocommit=True  
        )
        try:
            cursor = connection.cursor()

            # Check if the database exists
            cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{self.rds_db_name}'")
            if cursor.fetchone() is None:
                cursor.execute(f"CREATE DATABASE `{self.rds_db_name}`")
                print(f"Database {self.rds_db_name} created successfully.")
            else:
                print(f"Database {self.rds_db_name} already exists.")
        except Exception as e:
            print(f"Error checking/creating database: {str(e)}")
            raise
        finally:
            connection.close()

    def check_and_create_table(self):
        """Check if the table exists, if not, create it."""
        try:
            connection = self._connect()
            cursor = connection.cursor()

            # Create the table if it does not exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS image_metadata (
                    user_id VARCHAR(255) NOT NULL,
                    image_id VARCHAR(255) NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    upload_timestamp DATETIME NOT NULL,
                    s3_url VARCHAR(512) NOT NULL,
                    PRIMARY KEY (user_id, image_id)
                )
            """)
            print("Table `image_metadata` checked/created successfully.")
        except Exception as e:
            print(f"Error checking/creating table: {str(e)}")
            raise
        finally:
            connection.close()