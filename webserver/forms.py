#!/usr/bin/env python
# -*- coding: utf8 -*-
from django import forms
from .models import hostinfo

class UserForm(forms.Form):
    username = forms.CharField(label='',max_length=100,widget=forms.TextInput(
        attrs={'id': 'username','placeholder': 'User'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(
        attrs={'id': 'password','placeholder': 'Password'}))

class RegisterForm(forms.Form):
    isactive = [
        (0, '禁用'),
        (1, '启用'),
    ]
    add_user = forms.CharField(label='add_user',max_length=20,widget=forms.TextInput(
        attrs={'id': 'add_user', 'name': 'add_user','placeholder': '请输入用户名'}))
    add_password = forms.CharField(label='add_password',max_length=20,widget=forms.PasswordInput(
        attrs={'id': 'add_password','name': 'add_password', 'placeholder': '请输入密码'}))
    add_passwordtwo = forms.CharField(label='add_passwordtwo',max_length=20,widget=forms.TextInput(
        attrs={'id': 'add_passwordtwo','name': 'add_passwordtwo', 'placeholder': '请确认密码'}))
    add_email = forms.EmailField(label='add_email',max_length=20,widget=forms.TextInput(
        attrs={'id': 'add_email', 'name': 'add_email','placeholder': '请输入您的邮箱'}))
    add_isactive = forms.IntegerField(widget=forms.Select(choices=isactive))

class AlterForm(forms.Form):
    isactive = [
        (0, '禁用'),
        (1, '启用'),
    ]
    alter_email = forms.EmailField(label='add_email', max_length=20,initial='class', widget=forms.TextInput(
        attrs={'id': 'add_email', 'name': 'add_email', 'placeholder': '请输入您的邮箱'}))
    alter_isactive = forms.IntegerField(widget=forms.Select(choices=isactive))

class Ser_add(forms.Form):
    add_intip = forms.CharField(label='add_intip',max_length=50,widget=forms.TextInput(
        attrs={'id':'add_intip','name':'add_intip','placeholder':'请输入内网ip地址',}))
    add_extip = forms.CharField(label='add_intip', max_length=50, widget=forms.TextInput(
        attrs={'id': 'add_extip', 'name': 'add_extip', 'placeholder': '请输入外网ip地址', }))
    add_manufacturers =forms.CharField(label='add_manufacturers',max_length=30)

class hostadimnForm(forms.Form):
    fun_select = [
        ('cmd.run', 'cmd.run'),
        ('test.ping', 'test.ping'),
    ]
    hostlist = forms.ModelChoiceField(queryset=hostinfo.objects.all(),empty_label="*",to_field_name="hostname",widget=forms.Select(
        attrs={'id':'hostlist', 'class':'selectpicker show-tick form-control', 'name':'hostlist'}))
    funlist = forms.CharField(widget=forms.Select(
        choices=fun_select,attrs={'id':'funlist', 'class':'selectpicker show-tick form-control', 'name':'funlist'}))
    command = forms.CharField(label='命令',widget=forms.TextInput(
        attrs={'class':'form-control','id':'search_name', 'name':'command'}))

class monitorForm(forms.Form):
    monitorHost = forms.ChoiceField(label='监控主机',widget=forms.Select(
        attrs={'id':'monitorHost', 'class':'selectpicker show-tick form-control', 'name':'monitorHost'}))

class autoArrMinionForm(forms.Form):
    add_ip = forms.GenericIPAddressField(label='add_minion_ip',max_length=50,widget=forms.TextInput(
        attrs={'id':'add_minion_ip','name':'add_minion_ip','placeholder':'IP','class':'form-control'}))
    add_username = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'id': 'add_minion_username', 'placeholder': 'User', 'class': 'form-control'}))
    add_password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'id': 'add_minion_password', 'placeholder': 'Password', 'class': 'form-control'}))