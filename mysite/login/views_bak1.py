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

        login_form = UserForm(request.POST)

        # 要对登陆的用户名和密码合法性验证
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 长度
            # 字符合法
            try:
                user = User.objects.get(name=username)
            except:
                message = '用户不存在'
                print('用户不存在')
                return render(request, 'login/login.html', locals())

            if user.password == password:
                return redirect('/index/')
            else:
                message = '密码输入错误'
                print('密码输入错误')
                return render(request, 'login/login.html', locals())

        else:
            message = '非法输入'
            print('非法输入')
            return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


# 另外，这里使用了一个小技巧，Python内置了一个locals()函数，它返回当前所有的本地变量字典，
# 我们可以偷懒的将这作为render函数的数据字典参数值，就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
# 这样做的好处当然是大大方便了我们，但是同时也可能往模板传入了一些多余的变量数据，造成数据冗余降低效率。

def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    pass
    return redirect("/login/")





