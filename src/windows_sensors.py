from sensor_interface import Sensors, Process
import random

class WindowsProcess(Process):
    def get_cpu_percent(self) -> float:
        return random.random()

    def get_power_draw(self) -> float:
        return 0

class WindowsSensors(Sensors):
    def get_power_consumption(self) -> float:
        return 9

    def get_process_list(self) -> list[Process]:
        return [
            WindowsProcess("Process 1", 1),
            WindowsProcess("Process 2", 2),
            WindowsProcess("Process 3", 3),
            WindowsProcess("Process 4", 4),
            WindowsProcess("Process 5", 5),
            WindowsProcess("Process 6", 6),
            WindowsProcess("Process 7", 7),
        ]