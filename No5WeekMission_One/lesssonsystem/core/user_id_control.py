from conf import settings
data_base_dst = settings.FILE_BASE
import pickle
import os
"""这个文件用于管理db/user_db/目录下的stid_db 和 tcid_db.负责学员唯一编号,和讲师唯一编号的管理"""
# 学员ID数据结构,key关联value的数字部分,这样保证了id 在key ,value的同时唯一性
student_db = {"1": "ST00001", "2": "ST00002", "3": "ST00003", "666": "ST00666", "7777": "ST07777", "88888": "ST88888"}


class UserIdControlModule(object):

    def __init__(self, args):
        self.id = 0
        self.id_data = {}
        self.dst = args
    User_db_dst = "%s/%s" % (data_base_dst["path"], data_base_dst["dir_name3"])
    st_db_dst = data_base_dst["student_id_name"]
    tc_db_dst = data_base_dst["teacher_id_name"]

    def create_id(self):
        with open(self.dst, "wb") as wf:
            pickle.dump(self.id_data, wf)

    def set_id_data(self, args):
        self.id_data[self.id] = args

    def assigned_id(self, args):
        """

        :param args: 请求分配ID 的角色是谁? 0:学员 or 1:教师
        :return:
        """
        file_dst = None
        if args == 0:
            file_dst = "%s/%s" % (UserIdControlModule.User_db_dst, UserIdControlModule.st_db_dst)
        elif args == 1:
            file_dst = "%s/%s" % (UserIdControlModule.User_db_dst, UserIdControlModule.tc_db_dst)
        with open(file_dst, "rb") as rf:
            if os.path.getsize(file_dst) == 0:
                self.id = 1
            else:
                self.id_data = pickle.load(rf)
                self.id = len(self.id_data) + 1
        self.dst = file_dst

    def get_id(self):
        return self.id
