from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    avatar = models.FileField(verbose_name='用户头像', upload_to='avatar/', default='avatar/w.jpg')
    create_time = models.DateField(auto_now_add=True)
    blog = models.OneToOneField(to='Blog', null=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    site_name = models.CharField(verbose_name='个人站点名称', max_length=32)
    site_title = models.CharField(verbose_name='个人站点标题', max_length=32)

    def __str__(self):
        return self.site_name


class Category(models.Model):
    name = models.CharField(verbose_name='文章分类', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签', max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(verbose_name='文章标题', max_length=64)
    desc = models.CharField(verbose_name='文章简介', max_length=255)
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateField(verbose_name='发布时间', auto_now_add=True)
    up_num = models.BigIntegerField(verbose_name='点赞数', default=0)
    down_num = models.BigIntegerField(verbose_name='点踩数', default=0)
    comment_num = models.BigIntegerField(verbose_name='评论数', default=0)
    blog = models.ForeignKey(to='Blog', null=True)
    category = models.ForeignKey(to='Category', null=True)
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    tag = models.ForeignKey(to='Tag')
    article = models.ForeignKey(to='Article')


class UpAndDown(models.Model):
    is_up = models.BooleanField()
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')


class Comment(models.Model):
    content = models.CharField(verbose_name='评论内容', max_length=255)
    content_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    user = models.ForeignKey(to='UserInfo')
    article = models.ForeignKey(to='Article')
    parent = models.ForeignKey(to='self', null=True)