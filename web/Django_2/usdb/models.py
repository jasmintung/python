from django.db import models

# Create your models here.


class UserGroup(models.Model):
    uid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    uptime = models.DateTimeField(auto_now=True, null=True)


class UserInfo(models.Model):
    username = models.CharField(max_length=64, blank=True, verbose_name="用户名")
    password = models.CharField(max_length=32, help_text='pwd')
    email = models.EmailField(max_length=32, null=True)
    phone = models.CharField(max_length=32, null=True)
    user_type_choices = (
        (1, '超级用户'),
        (2, '普通用户'),
        (3, '一般用户'),
    )
    user_type_id = models.IntegerField(choices=user_type_choices, default=3)
    user_group = models.ForeignKey("UserGroup", to_field='uid', on_delete=models.CASCADE, default="")


class adminInfo(models.Model):
    username = models.CharField(max_length=64, verbose_name="用户名")
    password = models.CharField(max_length=32, help_text='pwd')
