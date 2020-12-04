#！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/12/4 9:44
# @Author   : Taylor
# @Software : PyCharm


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

if __name__ == '__main__':
    # send_mail(
    #     '来自www.liujiangblog.com的测试邮件',
    #     '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！',
    #     'hulei_pm@163.com',
    #     ['hulei_pm@163.com'],
    # )

    subject, from_email, to = '来自www.liujiangblog.com的测试邮件', 'hulei_pm@163.com', 'hulei_pm@163.com'
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.baidu.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()







