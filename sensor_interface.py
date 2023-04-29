class Process:
    def __init__(self, name: str, cpu_percent: float, power_draw: float):
        self.name = name
        self.cpu_percent = cpu_percent
        self.power_draw = power_draw

class Sensors:
    def get_power_consumption() -> float:
        '''Returns the power draw of the system in Watts
        '''
        pass

    def get_process_list() -> List[Process]:
        pass