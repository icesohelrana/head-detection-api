import yaml
import cv2
import torch
import numpy as np
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from utils.general import check_img_size,non_max_suppression,scale_coords
from models.experimental import attempt_load

from function.S3 import S3
import os

stride = int(model.stride.max())
with open('config.yaml') as f:
    config = yaml.safe_load(f)
detection_config = config["DETECTION"]
model = attempt_load(detection_config["MODEL_PATH"], map_location='cpu')

s3 = S3()
app = Flask(__name__)
api = Api(app)  # Initialize Flask-RESTful

# Define a request parser to handle input data in JSON format
parser = reqparse.RequestParser()
parser.add_argument('img_path', required=True)  # Expect 'data' key in JSON


class inference(Resource):
    def post(self):
        args = parser.parse_args()
        img_path = args['img_path']

        img0 = s3.download_image_from_s3(img_path)
        img = cv2.resize(img0,(detection_config['IMG_SIZE'],detection_config['IMG_SIZE']))
        img = torch.tensor(img).float()
        # img = img.half()
        img = img.unsqueeze(0)
        img /= 255.0
        img = img.permute(0,3,1,2)
        pred = model(img, augment=True)[0]
        pred = non_max_suppression(pred, detection_config['CONF_THRESH'],detection_config['IOU_THRESH'], classes=[0], agnostic=True)
        det = pred[0]
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()


        return jsonify({'detection': det.tolist()})

api.add_resource(inference, '/predict')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
