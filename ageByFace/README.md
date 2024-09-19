# Age and Gender Detector

In this example, we are going to give you a model which can predict gender and age by giving your face to it. Beside the model that is presented, a small app has been written to connect to your camera and predict for the faces in front of camera.

## Pre-required packages

To use this code you should install the following packages for python using the following command

```bash
pip install tensorflow torch pandas numpy opencv-python yolo5 keras matplotlib
```

Besides packages that you have installed, if you want to train the model again, you should download the dataset from [kaggle](https://www.kaggle.com/datasets/jangedoo/utkface-new). Then, extract UTKFaces folder where the scripts are located. 

If you only want to use the code to read read from camera and predict the faces, you should first download model h5 file from [Google Drive](https://drive.google.com/file/d/1HFO0s-KCSh9HknCz9ysuSeERCpJDwFek/view?usp=drive_link), then put it where `faceDetector.py` file is located. 

## How to Run

The porpuse of this example is to get data from camera and detect faces in the camera and predict age and gender of any faces inside it. after downloading the files and packages that has been said in `pre-required packages` section, if you want to train the model, you should run the jupyther file `age_gender_model.ipynb`. If you don't want to train, run `faceDetector.py` script with the following command.
```bash 
python faceDetector.py
```
At first, it may take a liitle to download YoLo model. After that, a window of camera will pop-up. A rectangle will be draw around every face and a label will be on top of rectangle that will show age and gender of detected face.