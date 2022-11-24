import re
import subprocess

FREQ_OFFSET = 7500
MEM_OFFSET = 1000
PATT = r"nvidiaInspector.exe \"-setVoltagePoints:(.*)\|\""
FMT_VFPOINT = "nvidiaInspector.exe -setVoltagePoints:{}"
FMT_MEMORY = "nvidiaInspector.exe -setMemoryClockOffset:0,0,{}"

subprocess.run(["nvidiaInspector.exe", "-dumpVoltagePoints:0"], check=True).check_returncode()
with open("setVoltagePoints.bat", "r", encoding="utf-8") as f:
    raw_cmd = f.readline().strip()

voltage_points = re.findall(PATT, raw_cmd)[0].split("|")
for i, point in enumerate(voltage_points):
    pre, post = point.split(";")
    post = str(int(post) + FREQ_OFFSET)
    voltage_points[i] = ";".join((pre, post))

ret = "|".join(voltage_points)

subprocess.run(FMT_MEMORY.format(MEM_OFFSET).split(), check=True).check_returncode()
subprocess.run(FMT_VFPOINT.format(ret).split(), check=True).check_returncode()
