class StrKeyDict0(dict):

    def __missing__(self, key):  # 找不到的键
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


# 优化

import collections


class StrKeyDict(collections.UserDict):

    def __missing__(self, key):
        if isinstance(self, key):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):  # 把所有键转换成字符串
        self.data[str(key)] = item
