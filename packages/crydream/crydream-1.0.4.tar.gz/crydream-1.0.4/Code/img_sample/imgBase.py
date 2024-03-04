import os

import cv2 as cv
import numpy as np


class Img_base:

    def __init__(self):
        roi_pos = [
            [0, 250], [0, 2500]  
        ]
        self.roiPos = roi_pos
        self.gray_value = 0
        self.gray_round = 0

    def rotate_img(self, img, angle):
        
        h, w = img.shape[:2]
        rotate_center = (w / 2, h / 2)
        M = cv.getRotationMatrix2D(rotate_center, angle, 1.0)
        new_w = int(h * np.abs(M[0, 1]) + w * np.abs(M[0, 0]))
        new_h = int(h * np.abs(M[0, 0]) + w * np.abs(M[0, 1]))
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2
        rotated_img = cv.warpAffine(img, M, (new_w, new_h))
        return rotated_img

    def sum_gray(self, img, x, y, radius):
        
        gray_number = 0  
        gray_sum = 0  
        x_InitialPoint = x - radius  
        y_InitialPoint = y - radius  
        if (x + radius) >= img.shape[0] or (y + radius) >= img.shape[1]:
            return 0
        else:
            for i in range(radius * 2 + 1):
                for j in range(radius * 2 + 1):
                    gray_number += 1
                    gray_sum += img[x_InitialPoint + i, y_InitialPoint + j]
        return gray_sum  

    def sum_gray_ave(self, img, x, y, radius):
        
        gray_number = 0  
        gray_sum = 0  
        gray_ave = 0
        x_InitialPoint = x - radius  
        y_InitialPoint = y - radius  
        if (x + radius) >= img.shape[0] or (y + radius) >= img.shape[1]:
            return 0
        else:
            for i in range(radius * 2 + 1):
                for j in range(radius * 2 + 1):
                    gray_number += 1
                    gray_sum += img[x_InitialPoint + i, y_InitialPoint + j]
        gray_ave = int(gray_sum / gray_number * 100) / 100
        return gray_ave  

    def clear_cache(self, path):
        os.remove(path)

    def get_gray_round(self, img):
        
        gray_number = 0  
        gray_sum = 0  
        gray_ave = 0  
        x_InitialPoint = 800  
        x_length = 600  
        y_InitialPoint = 300  
        y_length = 100  
        img_array = np.transpose(np.array(img))
        for i in range(x_length):
            for j in range(y_length):
                gray_number += 2
                gray_sum += img_array[x_InitialPoint + i, y_InitialPoint + j]
                gray_sum += img_array[x_InitialPoint + i, y_InitialPoint + 4700 + j]
        gray_ave = gray_sum / gray_number
        self.gray_round = int(gray_ave * 100) / 100
        num = int(gray_ave / 10) * 10 + 100

        return num

    def point_X(self, min, mid, max):
        
        point = [0] * 5
        point[0] = min
        point[1] = min + (mid - min) / 2
        point[2] = mid
        point[3] = max - (max - mid) / 2
        point[4] = max
        return point

    def find_min_value(self, arr):
        
        arr = np.delete(arr, 0, axis=0)
        min_value = arr[0][0]
        for row in arr:
            for num in row:
                if num < min_value:
                    min_value = num
        print("背景值-扣除：", int(min_value))
        return min_value

    def nature_positive_negative(self, g_arr, n_arr):
        
        for i in range(9):
            for j in range(5):
                if i > 0:
                    if g_arr[i][j] < 60000:
                        n_arr[i][j] = "阴性"
                    elif g_arr[i][j] < 660000:
                        n_arr[i][j] = "弱阳性"
                    elif g_arr[i][j] < 1100000:
                        n_arr[i][j] = "中阳性"
                    elif g_arr[i][j] > 1100000:
                        n_arr[i][j] = "强阳性"
                    else:
                        n_arr[i][j] = "error"
        return n_arr

class Img_show:

    def __init__(self):
        pass

    def img_read(self, path_read):
        
        img_original = cv.cvtColor(cv.imread(path_read), cv.COLOR_RGB2GRAY)
        (w, h) = img_original.shape[:2]
        if w == 5472 and h ==5472:
            center = (w // 2, h // 2)
            M = cv.getRotationMatrix2D(center, -90, 1.0)
            img_original = cv.warpAffine(img_original, M, (w, h))
            img_original = img_original[0:w, (h - 2300):h]
        else:
            pass

        return img_original

    def img_dst(self, img, dat_num):
        
        ret, img_thres = cv.threshold(img, dat_num, 255, cv.THRESH_BINARY)

        return img_thres

    def img_erosion(self, img, num_erosion):
        
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_erosion, num_erosion))
        img_erosion = cv.erode(img, kernel)

        return img_erosion

    def img_dilation(self, img, num_dilation):
        
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (num_dilation, num_dilation))
        img_dilation = cv.dilate(img, kernel)

        return img_dilation
