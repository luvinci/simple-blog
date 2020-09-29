### 如何运行？

先创建一个数据库，名为：pdsite，可以在settings中修改。

> 安装环境

```
pip install pipreqs
pip install -r requirements.txt
```

> 启动方式1

- 直接将根目录下的`pdsite.sql`，导入数据库。

- 运行`python manage.py runserver`启动服务即可。

    因为此sql文件包含了管理员账户和一些初始化文章：

    ```
    管理员账号：admin
    管理员密码：abcd1234
    ```

> 启动方式2

同步数据库表和创建管理员账户。

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

在创建好管理员账户后，如果要使用管理员账户发表一些文章，则还需要做一些操作。

登陆`ip:port/admin`，点击BLOG下的Users，进去后点击admin，拉到最下面，设置`昵称`，如果不设置昵称，前台展示名称将为None，保存。

然后点击上面的`Home`路径回到原来的页面，点击BLOG下的Blogs，点击admin，进去后设置`个人博客名称`（不设置的话，在前台页面直接访问文章发表会报错，因为使用python manage.py createsuperuser创建的账户不像前台注册的账户那样可以直接关联了博客表）和个人博客后缀名（随便填，不为空即可），记得保存。

最后`python manage.py runserver`启动服务。





























