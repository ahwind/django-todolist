# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate,login as user_login,logout
from django.shortcuts import HttpResponseRedirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def Logout(request):
    logout(request)
    response = HttpResponseRedirect('/')
    return response


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            messages.info(request, u'用户名或密码不能为空！')
            return render(request, 'login.html', locals())

        user = authenticate(username = username,password = password)
        if user is not None and user.is_active:

            user_login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, u'用户名或密码错误！')
            return render(request, 'login.html',locals())
    else:
        return render(request, 'login.html')

