from ultralytics import YOLO
import cv2
import math
from deepface import DeepFace
from PIL import Image
global result_list
import time
t = time.time()
def calculate_distance(bbox1, bbox2):
    x1_c, y1_c = (bbox1[0] + bbox1[2]) / 2, (bbox1[1] + bbox1[3]) / 2  # Centroid of bbox1
    x2_c, y2_c = (bbox2[0] + bbox2[2]) / 2, (bbox2[1] + bbox2[3]) / 2  # Centroid of bbox2
    
    # Euclidean distance formula
    distance = math.sqrt((x2_c - x1_c) ** 2 + (y2_c - y1_c) ** 2)
    
    return distance

model = YOLO("yolov5s.pt")
result_list=[]
cap = cv2.VideoCapture("rohan.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Video writer
video_writer = cv2.VideoWriter("check.mp4",
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               fps,
                               (w, h))
video_writer1 = cv2.VideoWriter("whole_detection.mp4",
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               fps,
                               (w, h))
while cap.isOpened() and (time.time()-t)<100:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform person detection
    results = model(frame)

    # Enumerate through detections
    for i, r in enumerate(results):
        im_bgr = r.plot() 
        im_rgb = Image.fromarray(im_bgr[..., ::-1]) 

        for i in range(len(r.names)):
            if(r.boxes[i].cls[0] == 0):
                print("Person detected in frame", i)
                break
        person_coords = r.boxes.xyxy[i][:4]
        face_coordinates = r.boxes.xyxy[i][:4].cpu().numpy().astype(int)
        face_crop = frame[face_coordinates[1]:face_coordinates[3], face_coordinates[0]:face_coordinates[2]]
        result = DeepFace.analyze(face_crop, actions=['emotion'], enforce_detection=False)
        print(result)
        result_list.append(result)
        # print("Person coordinates:", person_coords)
        for i in range(len(r.boxes)):
            # print(r.names)
            # print(r.boxes[i])
            if(r.boxes[i].cls[0] == 0 or r.boxes[i].cls[0]!=63):
                continue
            obj_coord = r.boxes.xyxy[i][:4]
            dist = calculate_distance(person_coords, obj_coord[:4])
            # print(dist)
            if dist < 300:
                    # Take action, e.g., draw bounding boxes or perform some other operation
                x1, y1, x2, y2 = map(int, obj_coord[:4])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red bounding box indicating contact

    # Write frame to video
    video_writer.write(frame)
    video_writer1.write(im_bgr)

video_writer.release()
cv2.destroyAllWindows()
