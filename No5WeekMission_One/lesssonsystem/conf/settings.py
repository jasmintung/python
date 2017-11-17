import os

BASE_FILES_DIR = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))

FILE_BASE = {
    "path": "%s/db" % BASE_FILES_DIR,
    "dir_name1": "admin_db",
    "dir_name2": "course_choosing_sys_db",
    "dir_name3": "user_db",
    "dir_name3_1": "student_db",
    "dir_name3_2": "teacher_db",
    "admin_file_name": "admin_account",
    "class_file_name": "class.db",
    "course_file_name": "course.db",
    "school_file_name": "school.db",
    "student_file_name": "student.db",
    "teacher_file_name": "teacher.db",
    "student_id_name": "stid_db",
    "teacher_id_name": "tcid_db"
}