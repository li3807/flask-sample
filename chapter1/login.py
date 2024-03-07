from flask_wtf import FlaskForm
from wtforms import validators, PasswordField, SubmitField, EmailField, BooleanField, DateField, \
    DateTimeField, DecimalRangeField, RadioField, FileField, Form


class LoginUserForm(FlaskForm):
    email = EmailField('登陆邮箱',
                       validators=[validators.data_required(), validators.email(message="请输入注册的邮箱地址")],
                       description="穷输入")
    password = PasswordField('登录密码', validators=[validators.data_required(),
                                                     validators.length(min=8, max=12, message="密码最少8位，最多12位。")])
    boolean = BooleanField('确认查看协议')
    date = DateField("选择日期")
    dateTime = DateTimeField("选择日期和时间")
    range = DecimalRangeField("请选择范围")
    radio = RadioField("单选按钮", choices=[("1", "C++"), ("0", "C"), ("2", "C#")], coerce=int, default=0)
    file = FileField("请选择文件")
    submit = SubmitField("登录")

