from django.db import models

# Create your models here.


class UserGroup(models.Model):
    uid = models.AutoField(primary_key=True)  # 为模型创建一个自增长的字段,具体自增操作由数据库完成
    caption = models.CharField(max_length=32, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True)  # 无论添加或者修改对象,时间为添加或者修改的时间
    uptime = models.DateTimeField(auto_now=True, null=True)  # 为添加时的时间,更改对象时不会有变动


class UserInfo(models.Model):
    # id列, 自增, 主键
    # 用户名列, 字符串类型, 指定长度
    username = models.CharField(max_length=32, blank=True, verbose_name='用户名')  # verbose_name:显示字段中文
    password = models.CharField(max_length=64, help_text='pwd')  # help_text:提示
    email = models.CharField(max_length=60, null=True)
    test = models.EmailField(max_length=19, null=True, error_messages={'invalid': '请输入密码'})
    # 外键关联,在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错
    user_group = models.ForeignKey("UserGroup", to_field='uid', on_delete=models.CASCADE, default="")
    user_type_choices = (
        (1, '超级用户'),
        (2, '普通用户'),
        (3, '一般用户'),
    )
    user_type_id = models.IntegerField(choices=user_type_choices, default=1)
