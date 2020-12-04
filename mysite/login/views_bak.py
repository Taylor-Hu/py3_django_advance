from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from .models import User
from .forms import UserForm

def index(request):
    pass
    # 会自己在app的templates目录下去找
    return render(request, 'login/index.html')


def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        # 要对登陆的用户名和密码合法性验证
        if username.strip() and password:
            # 长度
            # 字符合法
            try:
                user = User.objects.get(name=username)
            except:
                message = '用户不存在'
                print('用户不存在')
                return render(request, 'login/login.html', {'message': message})

            if user.password == password:
                return redirect('/index/')
            else:
                message = '密码输入错误'
                print('密码输入错误')
                return render(request, 'login/login.html', {'message': message})

        else:
            message = '非法输入'
            print('非法输入')
            return render(request, 'login/login.html', {'message': message})


    return render(request, 'login/login.html')


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    pass
    return redirect("/login/")





