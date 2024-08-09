from ultralytics import YOLO

# # Load a model
model = YOLO("yolov8x-seg_custom.yaml")  # build a new model from scratch

# #model = YOLO("yolov8n-seg.pt")  # load a pretrained model (recommended for training)

# # Use the model
results = model.train(data="custom_data.yaml", epochs=5, workers=1, batch=8,imgsz=640)


# #"C:/Users/SAI GANESH S/Desktop/ultra_analytics/dental_image/train/images/IMG_3877.PNG"
# #"C:/Users/SAI GANESH S/Desktop/ultra_analytics\best.pt"



# from ultralytics.utils import ASSETS
# from ultralytics.models.yolo.segment import SegmentationPredictor

# args = dict(model='C:/Users/SAI GANESH S/Desktop/ultra_analytics/best.pt', source="C:/Users/SAI GANESH S/Desktop/ultra_analytics/dental_image/train/images/IMG_3877.PNG")
# predictor = SegmentationPredictor(overrides=args)
# predictor.predict_cli()