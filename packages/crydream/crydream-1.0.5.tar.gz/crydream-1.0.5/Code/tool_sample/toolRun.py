import platform


class python_tool:

    def __init__(self):
        pass

    #   1 系统检测
    def system_platform(self):
        #   系统信息标注
        system_info = [
            ['Linux', 'aarch64'],  # 嵌入式主控
            ['Windows', 'AMD64'],  # Windows主机
            ['Linux', 'X86_64']  # Linux主机
        ]
        #   获取系统ID
        system_id = platform.system()
        #   获取CPU的ID
        machine_id = platform.machine()
        #   判定是否为嵌入式主控
        if system_id == system_info[0][0] and machine_id == system_info[0][1]:
            return True
        else:
            return False
