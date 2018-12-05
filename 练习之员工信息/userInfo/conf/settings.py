import os

BASE_DB = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))


DATABASE = {
    "engine": "file_storage",
    "name": "employinfo_storage",
    "path": "%s/db" % BASE_DB
}