from ultralytics import YOLO

model=YOLO()
model.train(data="C:/Users/SAI GANESH S/Desktop/ultra_analytics/dataset/data.yaml",epochs=150)


#C:\Users\SAI GANESH S\runs\detect\train3/best.pt


#predict code
# yolo task=detect mode=predict model="C:/Users/SAI GANESH S/Desktop/ultra_analytics/best.pt" conf=0.25 source="C:/Users/SAI GANESH S/Desktop/ultra_analytics/dataset/test/images"

#segement inbuilt cli command
#yolo task=segment mode=predict model=yolov8n-seg.pt source='emoji2.jpg'

#"C:/Users/SAI GANESH S/Desktop/ultra_analytics/face_dataset/valid/images/emoji4_jpg.rf.6aa1ce84254806c73327018e60dc037b.jpg"
