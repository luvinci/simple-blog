from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户表
    """
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(verbose_name="昵称", max_length=16, null=True, db_index=True)
    avatar = models.CharField(verbose_name="头像", max_length=64, default="media/avatars/default.jpg", db_index=True)
    reg_data = models.DateField(verbose_name="注册日期", auto_now_add=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客表
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(to="UserInfo", to_field="id", null=True, db_index=True)
    name = models.CharField(verbose_name="个人博客名称", max_length=64)
    site_postfix = models.CharField(verbose_name="个人博客后缀名", max_length=32, unique=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    分类表
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="分类名称", max_length=32)
    blog = models.ForeignKey(to="Blog", to_field="id")  # 一个博客站点可以有多个分类

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签表
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="标签名称", max_length=32)
    blog = models.ForeignKey(to="Blog", to_field="id")  # 一个博客站点可以有多个标签

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章表
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="文章标题", max_length=64)
    desc = models.CharField(verbose_name="文章描述", max_length=120)
    publish_time = models.DateTimeField(verbose_name="发表时间", auto_now_add=True)

    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    up_count = models.IntegerField(verbose_name="推荐数", default=0)
    down_count = models.IntegerField(verbose_name="反对数", default=0)

    blog = models.ForeignKey(to="Blog", to_field="id", null=True)
    category = models.ForeignKey(verbose_name="所属分类", to="Category", null=True)

    tags = models.ManyToManyField(
        verbose_name="所属标签",
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag")
    )

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    """
    文章和标签的m2m表
    """
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="id")
    tag = models.ForeignKey(to="Tag", to_field="id")

    class Meta:
        unique_together = [
            ("article", "tag"),
        ]

    def __str__(self):
        v = self.article.title + "--" + self.tag.name
        return v


class ArticleDetail(models.Model):
    """
    文章详情表
    """
    id = models.AutoField(primary_key=True)
    article = models.OneToOneField(to="Article", to_field="id")
    content = models.TextField(verbose_name="文章内容")

    def __str__(self):
        return self.article.title


class ArticleUpDown(models.Model):
    """
    点赞表（哪个用户对哪篇文章点了赞）
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="id", null=True)
    article = models.ForeignKey(to="Article", to_field="id", null=True)
    is_up = models.BooleanField(verbose_name="是否为赞", default=True)

    class Meta:
        unique_together = [
            ("user", "article"),
        ]


class Comment(models.Model):
    """
    评论表
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="id")
    article = models.ForeignKey(to="Article", to_field="id")
    content = models.CharField(verbose_name="评论内容", max_length=255)
    comment_time = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)
    parent_comment = models.ForeignKey(verbose_name="父评论", to="self", null=True)

    def __str__(self):
        return self.content

