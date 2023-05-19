from camera import camera
from public_method import *
from datetime import datetime
from time import sleep
import numpy as np
import cv2
import csv
import os


class Detection:
    def __init__(self):
        pass

    @staticmethod
    def get_detect_image(framerate, iso):
        cam = camera(framerate, iso)
        try:
            image, ss, ISO = cam.shot()
        finally:
            cam.close()

        # gray scaling
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Convert to graylevel...")
        image = crop(image)

        return image, ss, ISO

    @staticmethod
    def check_necessity():
        print("Check necessity...")
        for i in range(0, 16):
            if os.path.exists(f"./para/ROIs/ROI_{i+1}.bmp") is False:
                print(f"File 'ROI_{i+1}.bmp' does no exist!")
                return False
        if os.path.exists("./para/ROIs/ROI_of_all.bmp") is False:
            print("File ROI_of_all.bmp does not exist!")
            return False
        if os.path.exists("./para/cali_factor.csv") is False:
            print("File cali_factor.csv does not exist!")
            return False
        if os.path.exists("./para/ROIs/coordinates.csv") is False:
            print("File coordinates.csv does not exist!")
            return False
        print("Checking has done!")
        return True

    @staticmethod
    def detect(framerate, iso, image_file_name=None):
        sleep(1)
        detect_image, ss, ISO = Detection.get_detect_image(framerate, iso)
        cv2.destroyAllWindows()
        value = calculate_average(detect_image)
        if image_file_name:
            save_image_with_value(image_file_name, detect_image, value)
        else:
            save_image_with_value(datetime.now(), detect_image, value)
        write_to_csv("./result/detection.csv", value+[ss]+[ISO])
        return value
