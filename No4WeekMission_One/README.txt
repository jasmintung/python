Author: Tony Cheung
版本: v1.0
程序介绍: 整体软件结构完全使用Alex老师的案例进行布置。
        实现一个员工信息表,支持增 删 改 查操作。支持部分模糊查找,所支持的模糊操作都有打印提示

员工信息表格式: 进行数据操作时,必须按照如下字段的格式进行操作
starffId |    name   | age |    phone    | dept | enroll date(登记日期)
    1      Alex Li 22        13651054608    IT    2017-08-16
登陆账号存放在: db/accounts里面,符合json格式前提下，根据自己的需要手动增加修改都行,已存在用户登陆失败次数超过三次被锁定。
            {"用户名1": ["密码", 登陆失败次数], "用户名2": ["密码", 登陆失败次数]}
员工信息数据库:
            放在db目录下employinfo_storage里面
启动说明: 启动代码放在bin目录下面ep_info_sheet.py文件中
模糊查找: 支持(英文姓名, 修改日期)
