from django.db import models

# Create your models here.


class WorkGroup(models.Model):
    """
    所在工作组
    """
    gid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    uptime = models.DateTimeField(auto_now=True, null=True)


class UserInfo(models.Model):
    """
    用户信息
    """
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, blank=True, verbose_name="用户名")
    password = models.CharField(max_length=32, help_text='pwd')
    email = models.EmailField(max_length=32, null=True)
    phone = models.CharField(max_length=32, null=True)
    user_type_choices = (
        (1, '超级用户'),
        (2, '普通用户'),
        (3, '游客'),
    )
    user_type_id = models.IntegerField(choices=user_type_choices, default=3)
    user_group = models.ForeignKey("WorkGroup", to_field='gid', on_delete=models.CASCADE, default="")


class adminInfo(models.Model):
    """
    管理员信息
    """
    username = models.CharField(max_length=64, verbose_name="用户名")
    password = models.CharField(max_length=32, help_text='pwd')


class InterestGroups(models.Model):
    """
    兴趣小组,与用户表形成多对多关系
    """
    name = models.CharField(max_length=64, verbose_name="组名")
    r = models.ManyToManyField("UserInfo")

# 手动创建多对多关系,可灵活增加更多的字段
# class InterestGroupToUser(models.Model):
#     iobj = models.ForeignKey(to="InterestGroups", to_field='id')
#     uobj = models.ForeignKey(to="UserInfo", to_field='id')
#     xxx = models.CharField(max_length=128, null=True)
