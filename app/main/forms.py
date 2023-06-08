from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField,SelectField,TextAreaField
from wtforms.validators import *
from flask_wtf.file import *

class LoginForm(FlaskForm):
    username=StringField('用户名: ',validators=[DataRequired()])
    password=PasswordField('密码: ',validators=[DataRequired()])
    submit=SubmitField('登录')

class RegisterForm(FlaskForm):
    name=StringField('用户名: ',validators=[DataRequired()])
    password=PasswordField('密码: ',validators=[DataRequired()])
    repassword=PasswordField('确认密码: ',validators=[DataRequired()])
    submit=SubmitField('注册')

class ResetUsernameForm(FlaskForm):
    new_name=StringField('新用户名: ',validators=[DataRequired()])
    submit=SubmitField('提交')

class ResetPasswordForm(FlaskForm):
    ori_password=PasswordField("旧密码: ",validators=[DataRequired()])
    new_password=PasswordField("新密码: ",validators=[DataRequired()])
    repassword=PasswordField("确认密码: ",validators=[DataRequired()])
    submit=SubmitField('确认修改')

class SearchForm(FlaskForm):
    input=StringField('关键词：',validators=[DataRequired()])
    submit=SubmitField('搜索')

# class NewNoteForm(FlaskForm):
#     title=StringField('标题: ',validators=[DataRequired()])
#     content=TextAreaField('内容: ',validators=[DataRequired()])
#     submit=SubmitField('发布')

# class CommentForm(FlaskForm):
#     comment=TextAreaField('发布评论: ',validators=[DataRequired()])
#     submit=SubmitField('提交')

# class NewGameForm(FlaskForm):
#     title=StringField('标题: ',validators=[DataRequired()])
#     north_spark=StringField('北家黑桃: ')
#     north_heart=StringField('北家红心: ')
#     north_diamond=StringField('北家方片: ')
#     north_club=StringField('北家草花: ')

#     west_spark=StringField('西家黑桃: ')
#     west_heart=StringField('西家红心: ')
#     west_diamond=StringField('西家方片: ')
#     west_club=StringField('西家草花: ')
    
#     east_spark=StringField('东家黑桃: ')
#     east_heart=StringField('东家红心: ')
#     east_diamond=StringField('东家方片: ')
#     east_club=StringField('东家草花: ')
    
#     south_spark=StringField('南家黑桃: ')
#     south_heart=StringField('南家红心: ')
#     south_diamond=StringField('南家方片: ')
#     south_club=StringField('南家草花: ')

#     dealer=SelectField('发牌方: ',choices=['N','W','E','S',''])
#     value=SelectField('局况: ',choices=['NS','EW','NO','BO',''])

#     content=TextAreaField('附加内容: ')
#     submit=SubmitField('发布')

# class EditInfoForm(FlaskForm):
#     name=StringField('用户名: ',validators=[DataRequired()])
#     realname=StringField('真实姓名: ',validators=[DataRequired()])
#     mail=StringField('邮箱: ',validators=[DataRequired()])
#     remark=StringField('备注: ')
#     submit=SubmitField('提交')

# class SearchForm(FlaskForm):
#     keyword=StringField('标题或关键字: ',validators=[DataRequired()])
#     type=SelectField('类型: ',choices=['牌局','笔记','全部'])
#     submit=SubmitField('搜索')

# class AdminLoginForm(FlaskForm):
#     username=StringField('管理员: ',validators=[DataRequired()])
#     password=PasswordField('密码: ',validators=[DataRequired()])
#     submit=SubmitField('登录')

# class HeadLogoForm(FlaskForm):
#     head_logo=FileField('上传头像',validators=[FileRequired()])
#     submit=SubmitField('更新头像')

# class MessageForm(FlaskForm):
#     comment=TextAreaField('留言: ',validators=[DataRequired()])
#     submit=SubmitField('提交')