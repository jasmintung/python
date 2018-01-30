# 本次作业需求
高级FTP服务器开发：
1. 用户加密认证
2. 多用户同时登陆
3. 每个用户有自己的家目录且只能访问自己的家目录
4. 对用户进行磁盘配额、不同用户配额可不同
5. 用户可以登陆server后，可切换目录
6. 查看当前目录下文件
7. 上传下载文件，保证文件一致性
8. 传输过程中现实进度条
9. 支持断点续传


## 为了客户端和服务器端数据方便解析，自定义一个协议规范:
# protocol = {"account":"", "password":"", "cmd": "", "data": ""}
1、登陆
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "login"
data = "admin" 或者 "user"
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "login"
data = 登陆结果: 9: #账户异常,请联系客服  0: #账户不存在  1*默认用户home路径*默认用户home路径下的文件夹及文件名,管理员的话就是盘符根目录: #登陆成功  2: #账户名或者密码错误

2、访问
客户端--------------------------------------------->服务器(登陆成功后自动发送)
account = xxx
password = xxx
cmd = "view"
data = "要访问目录的绝对路径"  # 为什么是绝对路径,因为没有做可视化界面，如果父级目录跟子级目录名称相同,程序无法处理.
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "view"
data = 客户端请求访问目录路径下的子目录及所有文件(列表转字符串) or "没有访问权限!" or "路径不存在!"

3、下载
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "download"
data = 要下载文件的绝对路径
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "download"
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

4、上传
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "upload"
data = 要上传到服务器上的绝对目录路径(根据本项目路径权限规则,本软件暂时只支持用户上传到自己初始默认路径下面及下面的子目录中)*文件名*文件大小   # 星号隔开,客户端输入的时候请输入文件绝对路径
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "upload"
data = "READY" or "NOT_READY" or "FILE_ALREADY_EXISTS"
客户端--------------------------------------------->服务器
account = xxx
password = xxx
cmd = "uploading"
data = 文件数据
服务器--------------------------------------------->客户端
account = xxx
password = xxx
cmd = "uploading"
data = 结果("SUCCESS")or"(FAILE)*累积收到的文件大小
