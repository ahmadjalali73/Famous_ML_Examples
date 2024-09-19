import numpy as np
import cv2 as cv
from PIL import Image
from os.path import dirname, abspath, join
import tensorflow as tf
from keras.src.legacy.saving import legacy_h5_format
import torch
import warnings

warnings.filterwarnings('ignore')

def feature_ext(img):
    print(type(img), img.shape)
    img = np.resize(img, (128, 128))
    img = np.array(img)
    img = img.reshape((1, 128,128,1))
    img = img / 255.0
    return img

def main():
    cur_dir = dirname(abspath(__file__))
    model_path = join(cur_dir, 'age_gender_detection.h5')
    model = legacy_h5_format.load_model_from_hdf5(model_path, custom_objects={'mae': 'mae'})
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    face_detector = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    gender_dict = {0:'Male', 1:'Female'}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces = face_detector.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
        result = yolo_model(gray)
        if result:
            for x in result.pandas().xyxy[0].itertuples():
                if x.name == 'person':
                    cropImg=gray[int(x.ymin):int(x.ymax),int(x.xmin):int(x.xmax)]
                    image2predict = feature_ext(cropImg)
                    pred = model.predict(image2predict)
                    pred_gender = gender_dict[round(pred[0][0][0])]
                    pred_age = round(pred[1][0][0])
                    cv.rectangle(frame, (int(x.xmin), int(x.ymin)), (int(x.xmax), int(x.ymax)), (0, 255, 0), 2)
                    cv.putText(frame, f'{pred_gender}, {pred_age}', (int(x.xmin), int(x.ymin)-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

main()
