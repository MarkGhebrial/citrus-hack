from sensor_interface import Sensors, Process

import os
rootdir = '/proc'

clk_tc = int(os.sysconf("SC_CLK_TCK"))

class LinuxProcess(Process):

    def __init__(self, name: str, pid: int):
        Process.__init__(self, name, pid)
        self.proc_total = 0
        self.cpu_tot = 0
        self.prev_proc_total = 0
        self.prev_cpu_total = 0

    def process_total(self) -> float:
        try:
            # Open the stat file for the process
            f = open("/proc/" + str(self.pid) + "/stat", "r")
        except:
            return 0

        contents = f.readline()
        contents = contents.split(" ")

        utime = int(contents[13])#/clk_tc
        stime = int(contents[14])

        return float(utime + stime)

    def cpu_total() -> float:
        f = open("/proc/stat", "r")
        cputimes = f.readline()
        cputotal = 0

        for i in cputimes.split(" ")[2:]:
            i = int(i)
            cputotal += i

        return(float(cputotal))

    def get_cpu_percent(self) -> float:
        self.prev_proc_total = self.proc_total
        self.prev_cpu_total = self.cpu_tot

        self.proc_total = self.process_total()
        self.cpu_tot = LinuxProcess.cpu_total()

        return ((self.proc_total - self.prev_proc_total) / (self.cpu_tot - self.prev_cpu_total) * 100)


    def get_power_draw(self) -> float:
        pass

class LinuxSensors(Sensors):
    def get_power_consumption() -> float:
        '''Returns the power draw of the system in Watts
        '''

        f = open("/sys/class/power_supply/BAT0/power_now")
        microwatts = int(f.readline())
        return microwatts / 1000000

    # https://man7.org/linux/man-pages/man5/proc.5.html
    def get_process_list() -> list[Process]:
        out = []

        # Iterate through the process directories
        for process_dir in os.listdir("/proc"):
            try:
                # Open the stat file for the process
                f = open("/proc/" + process_dir + "/stat", "r")
            except:
                # If the stat file does not exist in the current directory,
                # that directory does not represent a process, so skip it
                continue
                
            contents = f.readline()
            contents = contents.split(" ")

            name = contents[1][1:-1]
            pid = int(contents[0]) # The name of the directory is the PID

            # Calculate the process' CPU usage

            utime = int(contents[13])#/clk_tc
            stime = int(contents[14])

            power_draw = 0
        
            out.append(Process(name, pid))#, cpu_percent, power_draw))

        return out

print(LinuxSensors.get_power_consumption())

procs = LinuxSensors.get_process_list()
firefox = None
for p in procs:
    if p.name == "firefox":
        firefox = p
        break

if firefox is None:
    exit(3)

firefox = LinuxProcess("firefox", 1188)

from time import sleep

while True:
    #print(firefox.process_total(), LinuxProcess.cpu_total())
    print(firefox.get_cpu_percent())
    sleep(0)

for proc in LinuxSensors.get_process_list():
    print(proc)
