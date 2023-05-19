from camera import camera
from public_method import *
from datetime import datetime
import numpy as np
import cv2
import math
import csv
import os

# parameters setting
thresholding_offset = 25 # you can get rid of the shadow region of the well by increasing it

def erode(image, kernel_para=3, iterations=1):
    kernel = np.ones((kernel_para, kernel_para), np.uint8)
    image_ero = cv2.erode(image, kernel, iterations=iterations)
    return image_ero


def dilate(image, kernel_para=3, iterations=1):
    kernel = np.ones((kernel_para, kernel_para), np.uint8)
    image_dil = cv2.dilate(image, kernel, iterations=iterations)
    return image_dil


def binarize(image):
    # the variable "thresholding_offset" is used to get rid of the shadow region that we aren't interested in 
    ret1, _ = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
    ret2, mask = cv2.threshold(image, ret1+thresholding_offset, 255, cv2.THRESH_BINARY)
    return mask


class Calibration:
    def __init__(self):
        pass

    @staticmethod
    def generate_mask(framerate, iso):
        """

        :return image:
        :return mask
        """
        cam = camera(framerate, iso)
        try:
            image, ss, ISO = cam.shot()
        finally:
            cam.close()

        # gray scaling
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Convert to graylevel...")
        image = crop(image)

        # binarization & processing
        mask = binarize(image)
        mask = dilate(erode(mask))
        return image, mask

    @staticmethod
    def get_center_coordinate_of_ROI(mask_of_image):
        """
        it will produce a csv file which contain coordinates of every wells
        :param mask_of_image:
        :return a list of coordinates of wells' center:
        """
        ret, binary = cv2.threshold(mask_of_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, hierachy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        uCon = []
        bCon = []
        radiusList = []

        for i, c in enumerate(contours):
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            perimeter = cv2.arcLength(c, True)
            radius = perimeter / (2 * math.pi)

            if len(radiusList):
                radiusList.append(int(radius))
            else:
                radiusList = [int(radius)]

            if i + 1 <= 8:
                if len(bCon):
                    bCon.append((cY, cX))
                else:
                    bCon = [(cY, cX)]
            else:
                if len(uCon):
                    uCon.append((cY, cX))
                else:
                    uCon = [(cY, cX)]
        uROI = sorted(uCon, key=lambda x: x[1], reverse=False)
        bROI = sorted(bCon, key=lambda x: x[1], reverse=False)
        coordinate_of_wells = uROI + bROI

        # write coordinates to csv file
        write_to_csv('./para/ROIs/coordinates.csv', coordinate_of_wells)

        return coordinate_of_wells, min(radiusList)-1

    @staticmethod
    def generate_ROI_pictures(mask):
        """

        :param mask:
        :return:
        """
        coordinate_of_wells, radius = Calibration.get_center_coordinate_of_ROI(mask)
        ROI_of_all = np.zeros(shape=mask.shape, dtype='uint8')
        ROI = [0] * 16
        num_of_pixels = 0
        for i, coor in enumerate(coordinate_of_wells):
            # create corresponding ROI of each wells
            ROI[i] = np.zeros(shape=mask.shape, dtype='uint8')
            # define calculate boundary
            start_point = [coor[0] - radius, coor[1] - radius]
            end_point = [coor[0] + radius, coor[1] + radius]

            for x in range(start_point[1], end_point[1] + 1):
                for y in range(start_point[0], end_point[0] + 1):
                    distance = ((x - coor[1]) ** 2 + (y - coor[0]) ** 2) ** 0.5
                    if distance <= radius and mask[y, x] == 255:
                        ROI[i][y, x] = 255
                        ROI_of_all[y, x] = 255
                        num_of_pixels += 1

            # save ROI_image
            cv2.imwrite(f'./para/ROIs/ROI_{i + 1}.bmp', ROI[i])
        cv2.imwrite('./para/ROIs/ROI_of_all.bmp', ROI_of_all)
        print("All ROI pictures are saved!")

        return None

    @staticmethod
    def get_calibration_para(value):
        # store factors to csv
        write_to_csv('./para/tmp/cali_factor.csv', value)
        print("Save calibration factors to 'cali_factor.csv'.")

        return None

    @staticmethod
    def calibrate(framerate, iso):
        image, mask = Calibration.generate_mask(framerate, iso)
        save_image_without_value(datetime.now(), image, save_folder='./para/result')
        if(len([name for name in os.listdir('./para/ROIs') if os.path.isfile(os.path.join('./para/ROIs', name))]) != 18):
            print("Generate ROI pictures...")
            Calibration.generate_ROI_pictures(mask)
        print("Calculate values...")
        value = calculate_average(image)
        Calibration.get_calibration_para(value)
        save_image_with_value(datetime.now(), image, value, save_folder='./para/result')
        return value
