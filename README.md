## Build a Flask API to fetch image from AWS S3 and run a inference for head detection on image

Download the head detection model parameters from here: [YOLOv5m-crowd-human](https://drive.google.com/file/d/1gglIwqxaH2iTvy6lZlXuAcMpd_U0GCUb/view?usp=sharing) .

Provide AWS access details and image stored S3 bucket name in config.yaml

###  Head & Person Detection Model 

Step 1: Build the docker container of model API
    
    sudo docker build -t head-detection .

Step 2: Run the docker container for head detection.

    sudo docker run --restart=always  
    -e AWS_ACCESS_KEY_ID=<aws_access_key_id>
    -e AWS_SECRET_ACCESS_KEY=<aws_secret_key_id>
    -e AWS_BUCKET_NAME=<s3_bucket_name_of_images>
    -p 5000:5000 head-detection -d

Step 3: Test the API. 

    curl -X POST -H "Content-Type: application/json" -d '{"img_path": "a_img.png"}' http://localhost:5000/predict

It will output few coordinates if the image contains visible person



[N.B. The head detection model is cloned from another repo]