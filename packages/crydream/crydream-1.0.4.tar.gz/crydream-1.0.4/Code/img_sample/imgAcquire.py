import os
import sys

import serial
import serial.tools.list_ports
from PIL import Image

import gxipy as gx




class Acq_Run:

    def __init__(self):
        self.Core = Acq_Core()

        Width_max = 5496
        Height_max = 3672
        self.Width_set = 1368  
        self.Height_set = 1150  
        self.OffsetX_set = [0, self.Width_set, self.Width_set * 2, self.Width_set * 3]
        self.OffsetY_set = [400, self.Height_set + 400]

        self.Com = ""
        self.ComRun_flag = False
        self.Print_Save = True

    def Led_init(self):
        self.ports_list = list(serial.tools.list_ports.comports())
        for comport in self.ports_list:
            if list(comport)[1][0:11] == "USB2.0-Ser！":
                self.Com = "%s" % comport[0]
                print("串口%s可用！" % self.Com)
            else:
                continue
        if self.Com != "":
            try:  
                self.ser = serial.Serial(self.Com, 9600)  
                self.ComRun_flag = True  
                print("串口初始化完成！")
                return True
            except Exception as e:  
                print("串口不可用！")
                print(e)
                return False
        else:  
            return False

    def Camera_init(self):
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            return False
        else:
            return True

    def img_cache(self, path_cache):
        self.Core.clear_cache(path_cache)
        flag = 0
        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            sys.exit(1)
        strSN = dev_info_list[0].get("sn")
        cam = device_manager.open_device_by_sn(strSN)
        cam.Width.set(self.Width_set)
        cam.Height.set(self.Height_set)
        cam.ExposureTime.set(60000.0)
        while (True):
            cam.OffsetX.set(self.OffsetX_set[flag % 4])
            cam.OffsetY.set(self.OffsetY_set[flag // 4])
            write_len = self.ser.write("$810001D".encode('utf-8'))
            cam.stream_on()
            raw_img = cam.data_stream[0].get_image(timeout=10000)
            write_len = self.ser.write("$810011C".encode('utf-8'))
            cam.stream_off()
            RGB_img = raw_img.convert("RGB")
            if RGB_img is None:
                continue
            print(flag, '1成功')
            numpy_img = RGB_img.get_numpy_array()
            if numpy_img is None:
                continue
            print(flag, '2成功')
            img = Image.fromarray(numpy_img, "RGB")
            img.save(path_cache + "img%s.jpeg" % flag)
            flag += 1
            print(flag, '3成功')
            if flag == 8 and self.Core.img_check(path_cache):
                cam.close_device()
                write_len = self.ser.write("$810011C".encode('utf-8'))
                break
            elif flag > 8:
                write_len = self.ser.write("$810011C".encode('utf-8'))
                flag = 0
        pass

    def img_acquire(self, path_cache, path_save, name):
        self.img_cache(path_cache)
        self.Core.img_merge(path_cache, path_save, name)
        return True


class Acq_Core:

    def __init__(self):
        pass

    def clear_cache(self, path_cache):
        for i in os.listdir(path_cache):
            os.remove(path_cache + "%s" % i)
        print("缓存图片全部删除")

    def img_check(self, path_cache):
        if len(os.listdir(path_cache)) == 8:
            print("图片获取完毕")
            return 1
        else:
            return 0

    def img_merge(self, path_cache, path_save, name):
        self.img_path = [path_cache + 'img0.jpeg', path_cache + 'img1.jpeg',
                         path_cache + 'img2.jpeg', path_cache + 'img3.jpeg',
                         path_cache + 'img4.jpeg', path_cache + 'img5.jpeg',
                         path_cache + 'img6.jpeg', path_cache + 'img7.jpeg']
        img = Image.open(self.img_path[0])
        width, height = img.size
        target_shape = (4 * width, 2 * height)
        target_shape_new = (4 * width, 4 * width)
        background = Image.new('L', target_shape)
        background_new = Image.new('L', target_shape_new)
        for i, img_num in enumerate(self.img_path):
            image = Image.open(img_num)
            image = image.resize((width, height))
            row, col = i // 4, i % 4
            location = (col * width, row * height)
            background.paste(image, location)
            background_new.paste(background, (0, 0))
        background_new.save(path_save + "%s.jpeg" % name)
        img.close()
        self.clear_cache(path_cache)
        pass
