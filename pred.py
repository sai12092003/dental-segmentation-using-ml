from ultralytics.utils import ASSETS
from ultralytics.models.yolo.segment import SegmentationPredictor

def run_prediction(image_path, output_path):
    args = dict(model='C:/Users/SAI GANESH S/Desktop/ultra_analytics/best200.pt', source=image_path, project=output_path, name="train/")
    predictor = SegmentationPredictor(overrides=args)
    predictor.predict_cli()


