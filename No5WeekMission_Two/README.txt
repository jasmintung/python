项目需求：
开发简单的FTP：
1. 用户登陆
2. 上传/下载文件
3. 不同用户家目录不同
4. 查看当前目录下文件
5. 充分使用面向对象知识

## 为了客户端和服务器端数据方便解析，特简单定义一个协议规范:
## protocol = {"account":"", "password":"", "cmd": "", "data": 0}
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