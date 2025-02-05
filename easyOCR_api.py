import easyocr
import cv2
import matplotlib.pyplot as plt
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import gpsd

class ImageHandler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def on_created(self, event):
        if event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            print(f"ตรวจพบไฟล์รูปภาพใหม่: {event.src_path}")
            self.process_image(event.src_path)
            self.get_location()

    def process_image(self, file_path):
        # ดึงพิกัดของเครื่องผ่าน Geolocation API
        # location = self.get_location()
        # print(f"พิกัดปัจจุบัน: {location}")

        # อัปโหลดหรือประมวลผลภาพเพิ่มเติม
        reader = easyocr.Reader(['th','en'])
        #img
        img = file_path

        result = reader.readtext(img,detail=0)
        count = 0
        print(result)


    def get_location(self):
        try:
            # Connect to the local gpsd
            gpsd.connect()
            # Get gps position
            packet = gpsd.get_current()
            # See the inline docs for GpsResponse for the available data
            print(packet.position())
        except Exception as e:
            print("ไม่สามารถดึงพิกัดได้:", e)
            return "ไม่ทราบพิกัด"

def monitor_folder(folder_path):
    event_handler = ImageHandler(folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_monitor = "D:\project\ocr\img"
    if not os.path.exists(folder_to_monitor):
        os.makedirs(folder_to_monitor)
    print(f"เริ่มการเฝ้าติดตามโฟลเดอร์ {folder_to_monitor}")
    monitor_folder(folder_to_monitor)





# reader = easyocr.Reader(['th','en'])

# #img
# img = cv2.imread('img\e4f3a30f-319c-4ebc-b016-d8ecefb124c7.jpeg')
# img2 = cv2.imread('D:\project\ocr\img\slip-history-05.jpg')

# result = reader.readtext(img2,detail=0)
# count = 0
# for i in result:
#     print(i, count)
#     count+=1
# cv2.imwrite('result.jpg',result)