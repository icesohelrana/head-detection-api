# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM python:3.10-bullseye

# Install linux packages
RUN apt update

# RUN apt-get install vim

# Install python dependencies
RUN python -m pip install --upgrade pip
RUN pip install torch==2.2.1 torchvision==0.17.1 --no-cache
RUN pip install opencv-python-headless seaborn matplotlib --no-cache
RUN pip install PyYAML==6.0.1 Flask Flask-RESTful boto3 requests tqdm scipy --no-cache


# Create working directory
WORKDIR /head-detection

# Copy contents

COPY . /head-detection
# EXPOSE 5000

ENTRYPOINT ["python", "/head-detection/single_image_inference.py"]
# Copy weights
#RUN python3 -c "from models import *; \
#attempt_download('weights/yolov5s.pt'); \
#attempt_download('weights/yolov5m.pt'); \
#attempt_download('weights/yolov5l.pt')"


# ---------------------------------------------------  Extras Below  ---------------------------------------------------

# Build and Push
# t=ultralytics/yolov5:latest && sudo docker build -t $t . && sudo docker push $t
# for v in {300..303}; do t=ultralytics/coco:v$v && sudo docker build -t $t . && sudo docker push $t; done

# Pull and Run
# t=ultralytics/yolov5:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus all $t

# Pull and Run with local directory access
# t=ultralytics/yolov5:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus all -v "$(pwd)"/coco:/usr/src/coco $t

# Kill all
# sudo docker kill $(sudo docker ps -q)

# Kill all image-based
# sudo docker kill $(sudo docker ps -qa --filter ancestor=ultralytics/yolov5:latest)

# Bash into running container
# sudo docker exec -it 5a9b5863d93d bash

# Bash into stopped container
# id=$(sudo docker ps -qa) && sudo docker start $id && sudo docker exec -it $id bash

# Send weights to GCP
# python -c "from utils.general import *; strip_optimizer('runs/train/exp0_*/weights/best.pt', 'tmp.pt')" && gsutil cp tmp.pt gs://*.pt

# Clean up
# docker system prune -a --volumes
