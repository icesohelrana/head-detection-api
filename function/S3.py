import boto3
import cv2
import numpy as np
class S3:
	def __init__(self,s3_config):
		try:
			self.s3_client = boto3.client('s3', aws_access_key_id=s3_config["AWS_ACCESS_KEY_ID"], 
							aws_secret_access_key=s3_config["AWS_SECRET_ACCESS_KEY"])
		except:
			print('s3 bucket connection failed')
		self.bucket_name = s3_config["S3_BUCKET_NAME"]
	def upload_frame_to_s3(self,frame,upload_path):
				# Encode frame as PNG (you can choose other formats)

		# Convert to byte array for S3 upload
		frame_data = frame.tobytes()

		# Specify key (filename) in S3 bucket
		s3_key = upload_path  # You can customize the naming scheme

		# Upload frame to S3
		self.s3_client.put_object(Body=frame_data, Bucket=self.bucket_name, Key=s3_key)
	def download_image_from_s3(self,image_path):
		response = self.s3_client.get_object(Bucket=self.bucket_name, Key=image_path)
		image_bytes = response['Body'].read()

		# Load image using cv2
		image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
		return image



