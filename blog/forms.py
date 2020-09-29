"""
基于Form组件实现登录注册校验
"""
import re
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from blog import models


def username_validate(value):
    """
    自定义规则，校验用户名
    :param value:
    :return:
    """
    pattern = re.compile(r"[a-zA-Z0-9_]{4,16}")
    if not pattern.match(value):
        raise ValidationError("用户名由数字、字母、下划线组成")


def email_validate(value):
    """
    自定义规则，校验邮箱
    :return:
    """
    pattern = re.compile(r"\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}")
    if not pattern.match(value):
        raise ValidationError("邮箱格式有误")


class AccountForm(forms.Form):
    nickname = forms.CharField(
        label="显示名称",
        required=True,
        max_length=16,
        widget=widgets.TextInput,
        error_messages={
            "required": "请输入显示名称",
            "max_length": "显示名称不能超过16位"
        },
    )
    username = forms.CharField(
        label="登录名称",
        required=True,
        min_length=4,
        max_length=16,
        widget=widgets.TextInput,
        error_messages={
            "required": "请输入登录名称",
            "min_length": "显示名称不能小于4位",
            "max_length": "显示名称不能超过16位",
        },
        validators = [username_validate,],
    )
    password = forms.CharField(
        label="密码",
        required=True,
        min_length=6,
        widget=widgets.PasswordInput,
        error_messages={
            "required": "请输入密码",
            "min_length": "密码不能小于6位"
        },
    )
    confirm_password = forms.CharField(
        label="确认密码",
        required=True,
        widget=widgets.PasswordInput,
        error_messages={
            "required": "请输入确认密码",
        },
    )
    email = forms.EmailField(
        label="邮箱",
        required=True,
        error_messages={
            "required": "请输入邮箱",
        },
        validators=[email_validate,],
    )

    def clean_username(self):
        """
        局部钩子
        :return:
        """
        black_list = ["sb", "sB", "Sb", "SB"]
        username = self.cleaned_data.get("username")
        for name in black_list:
            if username in name:
                raise ValidationError("登录名称不可含有敏感词语")
        obj = models.UserInfo.objects.filter(username=username)
        if obj:
            raise ValidationError("该用户已存在")
        return username

    def clean_email(self):
        """
        局部钩子
        :return:
        """
        email = self.cleaned_data.get("email")
        obj = models.UserInfo.objects.filter(email=email)
        if obj:
            raise ValidationError("该邮箱已存在")
        return email

    def clean(self):
        """
        全局钩子
        :return:
        """
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if confirm_password != password:
            # self.add_error("confirm_password", ValidationError("确认密码错误"))
            raise ValidationError("确认密码错误")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        """
        批量添加样式
        :param args:
        :param kwargs:
        """
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                "class": "form-control"
            })


class SetPassword(forms.Form):
    password = forms.CharField(
        label="密码",
        required=True,
        min_length=6,
        widget=widgets.PasswordInput,
        error_messages={
            "required": "请输入密码",
            "min_length": "密码不能小于6位"
        },
    )
    confirm_password = forms.CharField(
        label="确认密码",
        required=True,
        widget=widgets.PasswordInput,
        error_messages={
            "required": "请输入确认密码",
        },
    )
    def clean(self):
        """
        全局钩子
        :return:
        """
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if confirm_password != password:
            # self.add_error("confirm_password", ValidationError("确认密码错误"))
            raise ValidationError("确认密码错误")
        return self.cleaned_data


class SetNickname(forms.Form):
    nickname = forms.CharField(
        label="显示名称",
        required=True,
        max_length=16,
        widget=widgets.TextInput,
        error_messages={
            "required": "请输入显示名称",
            "max_length": "显示名称不能超过16位"
        },
    )
