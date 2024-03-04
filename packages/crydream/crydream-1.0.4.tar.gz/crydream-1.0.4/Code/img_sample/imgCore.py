import math
import operator

import cv2 as cv
import numpy as np

import imgBase


class Img_core:

    def __init__(self):
        self.Base = imgBase.Img_base()

        self.gray_down = 0
        self.dip_angle = 0

    def img_location_first(self, img_gray, img_dst, num, flag):
        
        num_down = 0  
        num_init = 500  
        len_down = 50  
        circle_x = []  
        circle_y = []  
        circle_r = []  
        for i in range(num):
            num_down = len_down * i + num_init  
            img_ROI = img_dst[(self.Base.roiPos[0][0] + num_down):(self.Base.roiPos[0][1] + num_down),
                      self.Base.roiPos[1][0]:self.Base.roiPos[1][1]]

            circle = cv.HoughCircles(img_ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
            if circle is None:
                continue
            elif circle.shape[1] < 3:
                continue
            elif circle.shape[1] >= 3:
                for i in range(circle.shape[1]):
                    circle[0][i][0] = circle[0][i][0] + self.Base.roiPos[1][0]
                    circle[0][i][1] = circle[0][i][1] + self.Base.roiPos[0][0] + num_down
                for j in circle[0, :]:
                    circle_x.append(j[0])
                    circle_y.append(j[1])
                    circle_r.append(j[2])

                exit_flag = 0

                circle_y_sort = sorted(circle_y, key=float)  
                diff_x1 = np.diff(circle_y_sort)  
                for i in range(len(diff_x1)):  
                    if diff_x1[i] > 200:
                        exit_flag = 1
                        break
                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：Y轴像素误差大于200")
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue

                circle_x_sort = sorted(circle_x, key=float)  
                diff_x2 = np.diff(circle_x_sort)  
                for i in range(len(diff_x2)):  
                    if diff_x2[i] < 630:
                        exit_flag = 1
                        break
                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：X轴像素误差小于630")
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue

                if circle.shape[1] == 3:  
                    gray_posi = np.zeros(1 * 3)  
                    img_array = np.transpose(np.array(img_gray))  
                    for j in range(3):
                        gray_posi[j] = self.Base.sum_gray_ave(img_array,
                                                              int(circle_x[j]),
                                                              int(circle_y[j]),
                                                              int(circle_r[j]))
                    min_index, min_number = min(enumerate(gray_posi), key=operator.itemgetter(1))
                    max_index, max_number = max(enumerate(gray_posi), key=operator.itemgetter(1))
                    if (max_number - min_number) >= 20:  
                        exit_flag = 1
                else:
                    gray_posi = np.zeros(1 * circle.shape[1])
                    exit_flag = 1

                if exit_flag != 0:
                    print("---------------------")
                    print("区间下移量：", num_down)
                    print("退出标志为：灰度均值不一致")
                    circle_x.clear()
                    circle_y.clear()
                    circle_r.clear()
                    continue
                else:
                    self.gray_down = num_down
                    print("---------------------")
                    print("* 初次获取定位点")
                    print("区间下移量：", num_down)
                    print("定位点X轴坐标：", circle_x)
                    print("定位点X轴差值：", diff_x2)
                    print("定位点Y轴坐标：", circle_y)
                    print("定位点直径：", circle_r)
                    print("定位点灰度值：", gray_posi)
                    if flag == 1:
                        cv.rectangle(img_gray,
                                     pt1=(self.Base.roiPos[1][0], self.Base.roiPos[0][0] + num_down),
                                     pt2=(self.Base.roiPos[1][1], self.Base.roiPos[0][1] + num_down),
                                     color=(0, 0, 0),
                                     thickness=20)
                        for j in circle[0, :]:
                            cv.circle(img_gray, (int(j[0]), int(j[1])), int(j[2]), (0, 0, 0), 10)
                    return 1, img_gray, circle, circle_x, circle_y
        return 0, img_gray, 0, circle_x, circle_y

    def img_correct_first(self, img_gray, img_dst, circle_x, circle_y):
        
        min_index, min_number = min(enumerate(circle_x), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(circle_x), key=operator.itemgetter(1))
        middle_index = None
        for i in range(3):
            if i == min_index or i == max_index:
                continue
            else:
                middle_index = i

        angle = math.atan2(circle_y[max_index] - circle_y[min_index], circle_x[max_index] - circle_x[min_index])
        angle = angle * 180 / math.pi
        self.dip_angle = angle  
        print("---------------------")
        print("定位点倾斜角度：", angle)
        img_rota = self.Base.rotate_img(img_gray, angle)
        img_rota_dst = self.Base.rotate_img(img_dst, angle)

        return img_rota, img_rota_dst, middle_index

    def img_correct_second(self, img_gray, img_dst, circle_x, circle_y, flag):
        
        cir_x = []  
        cir_out_x = []
        cir_y = []  
        cir_out_y = []
        cir_r = []
        exit_flag = 0  
        dis_error = 0  
        point_x = [0] * 5
        point_y = [450, 750, 1100, 1430, 1770, 2100, 2450, 2780]
        y_arve = int(sum(circle_y) / 3) - 100
        print("---------------------")
        print("参考点Y轴：", y_arve)
        ROI = img_dst[(y_arve):(y_arve + 200), 0:2500]
        circle = cv.HoughCircles(ROI, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50, maxRadius=150)
        if (circle is None) or (circle.shape[1] < 3):
            min_in, min_num = min(enumerate(circle_x), key=operator.itemgetter(1))
            max_in, max_num = max(enumerate(circle_x), key=operator.itemgetter(1))
            middle_index = None
            for i in range(3):
                if i == min_in or i == max_in:
                    continue
                else:
                    middle_index = i
            point_x = self.Base.point_X(min_num, circle_x[middle_index], max_num)
            print("试剂点X轴坐标：", point_x)
            for i in range(8):
                point_y[i] = int(y_arve + point_y[i])
            return point_x, point_y, dis_error, circle_x, circle_y
        for i in circle[0, :]:
            cir_x.append(i[0])
            cir_y.append(i[1] + y_arve)
            cir_r.append(i[2])
        print("矫正后定位点X轴坐标：", cir_x)
        print("矫正后定位点Y轴坐标：", cir_y)
        print("矫正后定位点直径：", cir_r)
        gray_posi = [0] * 3
        img_array = np.transpose(np.array(img_gray))  
        for j in range(3):
            gray_posi[j] = self.Base.sum_gray_ave(img_array, int(cir_x[j]), int(cir_y[j]), int(cir_r[j]))
        gray_ave = int((sum(gray_posi) / 3) * 100) / 100 - 20
        print("定位点灰度均值判读阈值：", gray_ave)

        if flag == 1:
            for j in circle[0, :]:
                cv.circle(img_gray, (int(j[0]), int(j[1] + y_arve)), int(j[2]), (0, 0, 0), 10)
            cv.rectangle(img_gray, pt1=(0, (y_arve)), pt2=(2500, (y_arve + 200)), color=(0, 0, 0), thickness=20)

        min_index, min_number = min(enumerate(cir_x), key=operator.itemgetter(1))
        max_index, max_number = max(enumerate(cir_x), key=operator.itemgetter(1))
        middle_index = None
        for i in range(3):
            if i == min_index or i == max_index:
                continue
            else:
                middle_index = i
        cir_out_x = [cir_x[min_index], cir_x[middle_index], cir_x[max_index]]
        cir_out_y = [cir_y[min_index], cir_y[middle_index], cir_y[max_index]]
        y_down = 2900
        ROI_Min = img_dst[(y_arve + y_down - 170):(y_arve + y_down + 170), int(min_number - 150):int(min_number + 150)]
        circle_min = cv.HoughCircles(ROI_Min, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
        ROI_Max = img_dst[(y_arve + y_down - 170):(y_arve + y_down + 170), int(max_number - 150):int(max_number + 150)]
        circle_max = cv.HoughCircles(ROI_Max, cv.HOUGH_GRADIENT, 0.5, 400, param1=100, param2=8, minRadius=50,
                                     maxRadius=150)
        print("---------------------")
        print("* 判断底部定位点情况")
        if circle_min is None and circle_max is None:
            print("底部全部定位点不存在")
            exit_flag = 3
        elif circle_min is None:
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            max_gray_aver = self.Base.sum_gray_ave(img_array, int(x_max), int(y_max), int(circle_max[0, :][0][2]))
            print("右侧定位点的灰度均值：", max_gray_aver)
            print("底部定位点右边点坐标：" + "(%d" % x_max + ",%d)" % y_max)
            if max_gray_aver <= gray_ave:
                exit_flag = 3
            else:
                exit_flag = 2
        elif circle_max is None:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            min_gray_aver = self.Base.sum_gray_ave(img_array, int(x_min), int(y_min), int(circle_min[0, :][0][2]))
            print("左侧定位点的灰度均值：", min_gray_aver)
            print("底部定位点左边点坐标：" + "(%d" % x_min + ",%d)" % y_min)
            if min_gray_aver <= gray_ave:
                exit_flag = 3
            else:
                exit_flag = 1
        else:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            min_gray_aver = self.Base.sum_gray_ave(img_array, int(x_min), int(y_min), int(circle_min[0, :][0][2]))
            max_gray_aver = self.Base.sum_gray_ave(img_array, int(x_max), int(y_max), int(circle_max[0, :][0][2]))
            print("左侧定位点的灰度均值：", min_gray_aver)
            print("右侧定位点的灰度均值：", max_gray_aver)
            print("底部定位点左边点坐标：" + "(%d" % x_min + ",%d)" % y_min)
            print("底部定位点右边点坐标：" + "(%d" % x_max + ",%d)" % y_max)
            if min_gray_aver <= gray_ave:
                exit_flag += 2
            if max_gray_aver <= gray_ave:
                exit_flag += 1

        print("---------------------")
        print("* 输出底部存在的定位点")
        if exit_flag == 0:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            cv.circle(img_gray, (int(x_min), int(y_min)), int(circle_min[0, :][0][2]), (0, 0, 0), 10)
            cv.circle(img_gray, (int(x_max), int(y_max)), int(circle_max[0, :][0][2]), (0, 0, 0), 10)
            dis_error = ((x_min - min_number) + (x_max - max_number)) / 2
            print("试剂点X轴坐标误差值：", dis_error)
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            y_arve_new = sum(cir_y) / 3
            y_down_ave = (y_max + y_min) / 2
            for i in range(8):
                point_y[i] = int(y_arve_new + (i + 1) * (y_down_ave - y_arve_new) / 8)
            print("试剂点Y轴坐标：", point_y)
            return point_x, point_y, dis_error, cir_out_x, cir_out_y
        elif exit_flag == 1:
            x_min = circle_min[0, :][0][0] + min_number - 150
            y_min = circle_min[0, :][0][1] + y_arve + y_down - 170
            cv.circle(img_gray, (int(x_min), int(y_min)), int(circle_min[0, :][0][2]), (0, 0, 0), 10)
            dis_error = x_min - min_number
            print("试剂点X轴坐标误差值：", dis_error)
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            y_arve_new = sum(cir_y) / 3
            y_down_ave = y_min
            for i in range(8):
                point_y[i] = int(y_arve_new + (i + 1) * (y_down_ave - y_arve_new) / 8)
            print("试剂点Y轴坐标：", point_y)
            return point_x, point_y, dis_error, cir_out_x, cir_out_y
        elif exit_flag == 2:
            x_max = circle_max[0, :][0][0] + max_number - 150
            y_max = circle_max[0, :][0][1] + y_arve + y_down - 170
            cv.circle(img_gray, (int(x_max), int(y_max)), int(circle_max[0, :][0][2]), (0, 0, 0), 10)
            dis_error = x_max - max_number
            print("试剂点X轴坐标误差值：", dis_error)
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            y_arve_new = sum(cir_y) / 3
            y_down_ave = y_max
            for i in range(8):
                point_y[i] = int(y_arve_new + (i + 1) * (y_down_ave - y_arve_new) / 8)
            print("试剂点Y轴坐标：", point_y)
            return point_x, point_y, dis_error, cir_out_x, cir_out_y
        else:
            point_x = self.Base.point_X(min_number, cir_x[middle_index], max_number)
            print("试剂点X轴坐标：", point_x)
            for i in range(8):
                point_y[i] = int(y_arve + point_y[i])
            print("试剂点Y轴坐标：", point_y)
            return point_x, point_y, dis_error, cir_out_x, cir_out_y

    def img_get_gray(self, img_rota, gray_aver, nature_aver, circle_x, circle_y, point_x, point_y,
                     dis_error, radius):
        
        img_array = np.transpose(np.array(img_rota))
        print("定位点X轴：", circle_x)
        print("定位点X轴：", circle_y)
        for i in range(3):
            print("定位点:", i + 1, circle_x[i], circle_y[i])  
            cv.circle(img_rota, (int(circle_x[i]), int(circle_y[i])), radius, (0, 0, 0), 10)
            gray_aver[0][i] = self.Base.sum_gray(img_array, int(circle_x[i]), int(circle_y[i]), radius)
        gray_aver[0][4] = gray_aver[0][2]
        gray_aver[0][2] = gray_aver[0][1]
        gray_aver[0][1] = 0
        for i in range(5):
            for j in range(8):
                cv.circle(img_rota, (int(point_x[i] + j * (dis_error / 8)), point_y[j]), radius, (0, 0, 0), 10)
                gray_aver[j + 1][i] = self.Base.sum_gray(img_array, int(point_x[i] + j * (dis_error / 8)), point_y[j],
                                                         radius)  
        min_blackgrand_value = self.Base.find_min_value(gray_aver)
        gray_aver = gray_aver - min_blackgrand_value
        nature_aver = self.Base.nature_positive_negative(gray_aver, nature_aver)

        return gray_aver, nature_aver, img_rota, 1
