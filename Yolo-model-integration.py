from flask import Flask, request, jsonify
import cv2
import torch

app = Flask(__name__)

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Video dimensions:
VIDEO_WIDTH = 3840
VIDEO_HEIGHT = 2160

LEFT_REGION = (0, 0, VIDEO_WIDTH // 2, VIDEO_HEIGHT) # persons
RIGHT_REGION = (VIDEO_WIDTH // 2, 0, VIDEO_WIDTH, VIDEO_HEIGHT) # vehicles

# Define object categories
PERSON_LABEL = 'person'
VEHICLE_LABELS = ['motorbike', 'bicycle']

def process_frame(frame):
    resized_frame = cv2.resize(frame, (640, 640))
    results = model(resized_frame)

    # Get original frame dimensions
    height, width, _ = frame.shape
    scale_x = width / 640
    scale_y = height / 640

    # Separate detections for persons and vehicles
    person_detections = []
    vehicle_detections = []

    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = [int(coord * scale_x if i % 2 == 0 else coord * scale_y) for i, coord in enumerate(box)]
        label = model.names[int(cls)]

        # Left region: Person detection
        if x1 < LEFT_REGION[2] and label == PERSON_LABEL:
            person_detections.append({
                'label': label,
                'confidence': float(conf),
                'box': [x1, y1, x2, y2]
            })

        # Right region: Vehicle detection
        elif x1 >= RIGHT_REGION[0] and label in VEHICLE_LABELS:
            vehicle_detections.append({
                'label': label,
                'confidence': float(conf),
                'box': [x1, y1, x2, y2]
            })

    return person_detections, vehicle_detections

@app.route('/detect', methods=['GET'])
def detect():
    
    video_source = r"C:\Users\ASUS\OneDrive\Desktop\portfolio\VID-20241016-WA0000.mp4" # specify the path where the input file is located

    if not video_source:
        return jsonify({'error': 'No video source provided'}), 400

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        return jsonify({'error': 'Cannot open video source'}), 400

    frame_results = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        persons, vehicles = process_frame(frame)
        frame_results.append({
            'persons': persons,
            'vehicles': vehicles
        })

    cap.release()
    return jsonify({'detections': frame_results})

if __name__ == '__main__':
    app.run(debug=True)