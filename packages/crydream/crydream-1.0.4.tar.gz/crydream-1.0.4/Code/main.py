import datetime
import os
import sys
import time

sys.path.append(os.path.dirname(__file__))

from em5822_sample.codeRun import em5822
from img_sample.codeRun import img
from .mount_sample.codeRun import mount


class Print_log:
    def __init__(self):
        self.em = em5822()
        self.img = img()
        self.mount = mount()
        self.Print_Save = True

        print("_______________________________________________")
        createFloder_path = [
            './dataset/img_result',
            './dataset/img_result/img_cache',
            './dataset/img_result/img_history',
            './dataset/img_result/img_input',
            './dataset/img_result/img_out',
            './dataset/img_result/img_tem',
            './logs',
            './logs/log_mount',
            './logs/log_em5822Init',
            './logs/log_em5822Run',
            './logs/log_LedInit',
            './logs/log_process',
            './logs/log_CameraInit',
            './logs/log_AcqRun'
        ]
        for i in createFloder_path:
            if not os.path.exists("%s" % i):
                os.makedirs("%s" % i)
                print("%s文件夹已经创建成功！" % i)
            else:
                print("%s文件夹已存在！" % i)

    def em5822_init_log(self):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./logs/log_em5822Init/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.em.emInit()

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    def em5822_out_log(self, Base, Nature, Data_Light):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./logs/log_em5822Run/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.em.emPrint(Base, Nature, Data_Light)

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    def Led_init_log(self):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("../logs/log_LedInit/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.img.ledInit()

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    def Camera_init_log(self):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./logs/log_CameraInit/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.img.camInit()

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    def Img_acquire_log(self, path_chache, path_save, name):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./logs/log_CameraInit/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.img.imgA(path_chache, path_save, name)

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag

    def Img_process_log(self, path_read, path_write, combina, radius):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./logs/log_process/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag, gray, nature = self.img.imgPro(path_read, path_write, combina, radius)

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass

        return flag, gray, nature

    def Move_log(self, original, final, identifier):
        start = time.perf_counter()  
        temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("./logs/log_mount/%s.log" % time_now, 'w')
            sys.stdout = Print_log
        else:
            pass

        flag = self.mount.mount(original, final, identifier)

        end = time.perf_counter()  
        print("时间消耗：%.2f s" % (end - start))

        if self.Print_Save == True:
            sys.stdout = temp
        else:
            pass
        return flag
