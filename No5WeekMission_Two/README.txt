项目需求：
开发简单的FTP：
1. 用户登陆
2. 上传/下载文件
3. 不同用户家目录不同
4. 查看当前目录下文件
5. 充分使用面向对象知识

## 为了客户端和服务器端数据方便解析，特简单定义一个协议规范:
## protocol = {"account":"", "password":"", "cmd": "", "data": ""}
## "cmd":["login","upload","download"] 支持的指令有：登陆，上传，下载
## 服务器返回：cmd == login
                data == 1: Real用户
                data == 2: Guest用户
                data == 9: Admin用户
                data == 0: 登陆失败
## 客户端，服务器端按照上述字典格式对bytes数据进行转换，以解析其数据内容
## FTP服务器端：普通用户自己的初始目录结构为：F:\XXX\XXXXXX\XXXX\用户名
## 所有用户在同一个目录层级
## 后续的代码编写,路径的解析也将严格根据上述描述的特征进行解析
## 下载保存的路径为:   C:\Users\Public\用户名\download文件夹下  可根据自己的使用情况在conf/settings里面进行配置
# bytes object
b = b"example"

# str object
s = "example"

# str to bytes
bytes(s, encoding = "utf8")

# bytes to str
str(b, encoding = "utf-8")

# an alternative method
# str to bytes
str.encode(s)

# bytes to str
bytes.decode(b)
1、登陆
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "login"
data = null
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "login"
data = 登陆结果: 1 REAL  2: GUEST  9  ADMIN  0 用户不存在  8 密码错误
2、浏览
客户端--------------------------------------------->服务器(登陆成功后自动发送)
account = xxx
password = xxx
cmd = "view"
data = null
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "view"
data = 默认初始访问目录绝对路径(字符串)*该目录路径下的子目录及所有文件(列表转字符串)

3、跳转路径
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "jump"
data = 要跳转到的路径名
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "jump"
data = 跳转访问目录绝对路径(字符串)*该目录路径下的子目录及所有文件(列表转字符串) or "no_permission" or "path_error"

4、下载
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "download"
data = 要下载文件的绝对路径
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "download_RES"
data = 下载的文件的总大小 or "file_not_exists"
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "download_RES"
data = "READY" or "NOT_READY" * 累计收到的文件数据量
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "download_ing"
data = 当前传送的文件
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "download_RES"
data = "READY" or "NOT_READY" * 累计收到的文件数据量       # 采用send发送,一应一答机制,为将来做补传机制做好基础

5、上传
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "upload"
data = 要上传到服务器上的绝对路径(根据本项目路径权限规则,本软件暂时只支持用户上传到自己初始默认路径下面及下面的子目录中)*文件名*文件大小   # 星号隔开,客户端输入的时候请输入文件绝对路径
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "upload_RES"
data = "READY" or "NOT_READY" or "FILE_ALREADY_EXISTS"
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "upload_RES"
data = "READY" or "NOT_READY"
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "upload_ing"
data = 结果("SUCCESS")or"(FAILE)*累积收到的文件大小
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "upload_ing"
data = 上传的文件数据
