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
data = 登陆结果
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
data = 默认初始访问目录*默认目录中的子目录及文件
3、向前浏览
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "next"
data = 要跳转到的具体的文件夹名字
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "next"
data = 当前文件夹下所有的子目录及文件信息的打印列表
4、向后浏览
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "prev"
data = 要跳转到的具体的文件夹名字
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "prev"
data = 当前文件夹下所有的子目录及文件信息的打印列表
5、下载
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "download"
data = 要下载文件的绝对路径(目录+文件名)
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "download"
data = 下载的文件的数据
6、上传
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "upload"
data = 要上传到服务器上的路径*要上传的文件的文件名*文件总大小    # 星号隔开
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "upload"
data = 收到的上传文件的数据大小     # 用于计算上传进度