#！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/12/2 17:42
# @Author   : Taylor
# @Software : PyCharm

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_loads.settings")

import django
if django.VERSION >= (1, 7):
    django.setup()


def main():
    from blog.models import Blog
    f = open('blog_db.txt')
    for line in f:
        title,content = line.split('****')
        # Blog.objects.create(title=title, content=content)
        Blog.objects.get_or_create(title=title, content=content)
    f.close()


if __name__ == '__main__':
    main()
    print('Done!')


