from sensor_interface import Sensors, Process

import os
import time

clk_tc = int(os.sysconf("SC_CLK_TCK"))

class LinuxProcess(Process):

    def __init__(self, name: str, pid: int):
        Process.__init__(self, name, pid)
        self.proc_total = 0
        self.cpu_tot = 0
        self.prev_proc_total = 0
        self.prev_cpu_total = 0

        self.get_cpu_percent()

    def process_total(self) -> float:
        try:
            # Open the stat file for the process
            f = open("/proc/" + str(self.pid) + "/stat", "r")
        except:
            return 0

        contents = f.readline()
        contents = contents.split(" ")

        utime = int(contents[13]) / clk_tc#/clk_tc
        stime = int(contents[14]) / clk_tc

        return float(utime + stime)

    def cpu_total() -> float:
        f = open("/proc/stat", "r")
        cputimes = f.readline()
        cputotal = 0

        for i in cputimes.split(" ")[2:]:
            i = int(i)
            cputotal += i

        return(float(cputotal)) / clk_tc

    def get_cpu_percent(self) -> float:
        self.prev_proc_total = self.proc_total
        self.prev_cpu_total = self.cpu_tot

        self.proc_total = self.process_total()
        self.cpu_tot = LinuxProcess.cpu_total()

        elapsed_process_time = self.proc_total - self.prev_proc_total
        elapsed_cpu_time = self.cpu_tot - self.prev_cpu_total

        # Don't divide by zero if no time has elapsed
        if elapsed_cpu_time == 0:
            return 0

        return (elapsed_process_time / elapsed_cpu_time * 100)


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

while True:
    #print(firefox.process_total(), LinuxProcess.cpu_total())
    print(firefox.get_cpu_percent())
    time.sleep(1)

for proc in LinuxSensors.get_process_list():
    print(proc)
