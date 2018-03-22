import os
import sys
pipei_str = "FtpClient.py"

cmd = "F:\CTO_week_mission\python\\No6WeekMission_Three\core\Server.py"
dirs = cmd.split("\\")
for i in dirs:
    print(i)
print(dirs[len(dirs) - 1])
file_name = dirs[len(dirs) -1]
file_dir = cmd[0:cmd.find(file_name)]
print(file_dir)
result = os.system(cmd)
print(result)
# result = os.popen("dir " + "F:\CTO_week_mission\python\\No6WeekMission_Three\core\Server.py")
#
# file_list = result.readlines()
# print(file_list)
# for info in file_list:
#     if pipei_str in info:
#         print(info)