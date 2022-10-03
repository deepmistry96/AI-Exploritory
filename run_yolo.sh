cd keras-yolo3
set MODELenv=model_data/yolo.h5
set ANCHORSenv=model_data\yolo_anchors.txt
set CLASSESenv=model_data\voc_classes.txt

python yolo_video.py --model %MODELenv% --anchors %ANCHORSenv% --classes %CLASSESenv% --image