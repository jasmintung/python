import re
from usdb import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets
from django.forms import fields


def mobile_validate(value):
    """
    自定义手机号格式校验,为了降低服务器请求压力,最好在前端对其进行校验,这里只是作为自己演示
    :param value:
    :return:
    """
    mobile_re = re.compile('^[1][3,4,5,7,8,9][0-9]{9}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class RFM(forms.Form):
    username = fields.CharField(
        error_messages={'required': '用户名不能为空'},  # 校验规则
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': "用户名", 'autocomplete': "off"})
    )
    password = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': "输入密码"})
    )
    password_2 = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': "再次输入密码"})
    )
    email = fields.EmailField(
        error_messages={'required': '邮箱不能为空', 'invalid': "邮箱格式错误"},
        widget=widgets.EmailInput(attrs={'class': "form-control", 'placeholder': "邮箱", 'autocomplete': "off"})
    )
    phone = fields.CharField(
        # validators=[checkphone],
        # validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^159[0-9]+$', '数字必须以159开头')],
        validators=[mobile_validate],  # 校验不起作用,暂时不知原因
        error_messages={'required': '手机号不能为空'},
        widget=widgets.Input(attrs={'class': 'form-control', 'placeholder': "手机号"})
    )
    u_type = fields.ChoiceField(
        label="角色类型",
        widget=widgets.Select(attrs={'class': 'form-control'}),
        choices=[(0, '超级用户'), (1, '普通用户'), (2, '游客')]
    )
    w_group = fields.ChoiceField(
        label="请选择工作组",
        widget=widgets.Select(attrs={'class': 'form-control'}),
        choices=models.WorkGroup.objects.all().values_list('gid', 'caption'),
    )
    i_group = fields.MultipleChoiceField(
        # label="请选择兴趣组(可多选)",  # 不知道为什么这句写上后,多选框不起作用
        # widget=widgets.Select(attrs={'class': 'form-control'}),  # 不知道为什么这句写上后,多选框不起作用
        choices=models.InterestGroups.objects.all().values_list('id', 'name')
    )
