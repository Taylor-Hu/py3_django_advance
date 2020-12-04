from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from .models import User, ConfirmString
from .forms import UserForm, RegisterForm
import hashlib

# hash加密
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):

    # 如果没有登陆应该跳转到登陆界面，index未登录限制访问；
    if not request.session.get('is_login', None):
        return redirect('/login/')


    # 会自己在app的templates目录下去找
    return render(request, 'login/index.html')


def login(request):
    # request.getSession(true)：若存在会话则返回该会话，否则新建一个会话。
    # request.getSession(false)：若存在会话则返回该会话，否则返回NULL
    if request.session.get('is_login', None):  # 避免重复登陆
        return redirect('/index/')

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

            if not user.has_confirmed:
                message = '该用户未经过邮箱确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
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
from django.conf import settings
def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'

    text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''<p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>'''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



# 注册时，进行注册码验证
import datetime
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


# 用户验证
def user_confirm(request):

    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '邮件已过期，请重新注册！'
        return render(request, 'login/register.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认！请使用账户登陆！'
        return render(request, 'login/confirm.html', locals())


def register(request):

    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():

            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '密码不一致'
                return render(request, 'login/register.html', locals())
            else:
                same_user = User.objects.filter(name=username)
                if same_user:
                    message = '用户已注册'
                    return render(request, 'login/register.html', locals())
                same_email = User.objects.filter(email=email)
                if same_email:
                    message = '邮箱已注册'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                # 以下内容新增加
                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
                # return redirect('login/')
        else:
            print('if---else, request.method=', request.method)
            return render(request, 'login/register.html', locals())

    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


# 编写了一个register.css样式文件
# form标签的action地址为/register/，class为form-register
# form中传递过来的表单变量名字为register_form
# 最下面的链接修改为直接登录的链接



def logout(request):
    if not request.session.get('is_login', None):
        # 如果没有登陆就要先登陆
        return redirect('/login/')

    request.session.flush()

    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    # 但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意。


    # # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect("/login/")





