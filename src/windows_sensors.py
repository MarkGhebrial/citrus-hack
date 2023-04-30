from sensor_interface import Sensors, Process
import random

import psutil

class WindowsProcess(Process):
    def __init__(self, psutil_proc: psutil.Process):
        self.psutil_proc = psutil_proc
        super().__init__(psutil_proc.name(), psutil_proc.pid)

    def get_cpu_percent(self) -> float:
        try:
            return psutil.Process(self.pid).cpu_percent(interval=0)
        except:
            return 0

    def get_power_draw(self) -> float:
        return 0

class WindowsSensors(Sensors):
    def __init__(self):
        self.process_list = []

    def get_power_consumption(self) -> float:
        return 9

    def get_process_list(self) -> list[Process]:
        new_process_list = []

        for pid in psutil.pids():
            try:
                new_process_list.append(WindowsProcess(psutil.Process(pid)))
            except:
                print("Process does not exist")
                pass

        # Add new processes to the list
        for new_proc in new_process_list:
            if new_proc not in self.process_list:
                self.process_list.append(new_proc)

        # Remopve dead processes from the list
        for old_proc in self.process_list:
            if old_proc not in new_process_list:
                self.process_list.remove(old_proc)

        return self.process_list