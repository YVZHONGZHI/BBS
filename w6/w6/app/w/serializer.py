import re
import os

from . import models
from bs4 import BeautifulSoup
from django.db.models import F
from django.contrib import auth
from django.conf import settings
from django.db import transaction
from django.db.models import Count
from rest_framework import serializers
from django.db.models.functions import TruncMonth
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


# LoginView

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        user_obj = self._get_user_obj(attrs)
        token = self._get_token(user_obj)
        self.context['user_obj'] = user_obj
        self.context['token'] = token
        return attrs

    def _get_user_obj(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            return user_obj
        raise ValidationError('用户名或密码错误!')

    def _get_token(self, user_obj):
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        return token


# RegisterView

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=3, max_length=8, allow_blank=True, write_only=True, error_messages={'min_length': '确认密码最少3位!', 'max_length': '确认密码最大8位!'})
    email = serializers.EmailField(allow_blank=True, error_messages={'invalid': '邮箱格式不正确!'})

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'email', 'avatar']
        extra_kwargs = {
            'username':{
                'min_length':3, 'max_length':8, 'allow_blank':True,
                'error_messages':{
                    'min_length': '用户名最少3位!',
                    'max_length': '用户名最大8位!'
                }
            },
            'password':{
                'min_length':3, 'max_length':8, 'allow_blank':True,
                'error_messages':{
                    'min_length': '密码最少3位!',
                    'max_length': '密码最大8位!'
                }
            }
        }

    def validate_username(self, attr):
        if not attr:
            raise ValidationError('用户名不能为空!')
        return attr

    def validate_password(self, attr):
        if not attr:
            raise ValidationError('密码不能为空!')
        if not re.match('^[0-9]+$', attr):
            raise ValidationError('密码不能为非数字!')
        return attr

    def validate_confirm_password(self, attr):
        if not attr:
            raise ValidationError('确认密码不能为空!')
        return attr

    def validate_email(self, attr):
        if not attr:
            raise ValidationError('邮箱不能为空!')
        return attr

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password == confirm_password:
            attrs.pop('confirm_password')
            return attrs
        raise ValidationError({'confirm_password': '两次输入的密码不一致!'})

    def create(self, validated_data):
        site_name = validated_data.get('username')
        category = ['的分类一', '的分类二', '的分类三']
        categories = []
        for w in category:
            categories.append(site_name + w)
        tag = ['的标签一', '的标签二', '的标签三']
        tags = []
        for w in tag:
            tags.append(site_name + w)
        site_title = validated_data.get('username') + '的博客'
        blog = models.Blog.objects.create(site_name=site_name, site_title=site_title)
        for name in categories:
            models.Category.objects.create(name=name, blog_id=blog.pk)
        for name in tags:
            models.Tag.objects.create(name=name, blog_id=blog.pk)
        validated_data['blog_id'] = blog.pk
        user_obj = models.UserInfo.objects.create_user(**validated_data)
        return user_obj


# CreatedView   SearchView

class CreatedSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='blog.site_name')
    site_title = serializers.CharField(source='blog.site_title')
    avatar = serializers.FileField(source='blog.userinfo.avatar')

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'desc', 'create_time', 'up_num', 'comment_num', 'site_name', 'site_title', 'avatar']


# SiteCreatedView

class LeftCategorySerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='blog.site_name')
    count_num = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'site_name', 'count_num']

    def get_count_num(self, instance):
        return instance.article_set.count()


class LeftTagSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='blog.site_name')
    count_num = serializers.SerializerMethodField()

    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'site_name', 'count_num']

    def get_count_num(self, instance):
        return instance.article_set.count()


class LeftMenuSerializer(serializers.ModelSerializer):
    category_list = LeftCategorySerializer(many=True, source='category_set')
    tag_list = LeftTagSerializer(many=True, source='tag_set')
    date_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Blog
        fields = ['site_title', 'category_list', 'tag_list', 'date_list']

    def get_date_list(self, instance):
        return models.Article.objects.filter(blog=instance).annotate(month=TruncMonth('create_time')).values('month').annotate(count_num=Count('pk')).values_list('month', 'count_num')


class SiteCreatedSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='blog.site_name')
    left_menu = LeftMenuSerializer(source='blog')

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'desc', 'create_time', 'up_num', 'comment_num', 'site_name', 'left_menu']


# ArticleDetailCreatedView

class ArticleDetailCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    parent = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'content_time', 'username', 'parent']

    def get_parent(self, instance):
        if instance.parent:
            return instance.parent.user.username
        return None


class ArticleDetailCreatedSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='blog.site_name')
    comment = ArticleDetailCommentSerializer(many=True, source='comment_set')
    left_menu = LeftMenuSerializer(source='blog')

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'content', 'up_num', 'down_num', 'site_name', 'comment', 'left_menu']


# SetPasswordView

class SetPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    old_password = serializers.CharField(allow_blank=True, write_only=True)
    new_password = serializers.CharField(min_length=3, max_length=8, allow_blank=True, write_only=True, error_messages={'min_length': '新密码最少3位!', 'max_length': '新密码最大8位!'})
    confirm_password = serializers.CharField(min_length=3, max_length=8, allow_blank=True, write_only=True, error_messages={'min_length': '确认密码最少3位!', 'max_length': '确认密码最大8位!'})

    class Meta:
        model = models.UserInfo
        fields = ['username', 'old_password', 'new_password', 'confirm_password']

    def validate_old_password(self, attr):
        if not attr:
            raise ValidationError('原密码不能为空!')
        return attr

    def validate_new_password(self, attr):
        if not attr:
            raise ValidationError('新密码不能为空!')
        if not re.match('^[0-9]+$', attr):
            raise ValidationError('新密码不能为非数字!')
        return attr

    def validate_confirm_password(self, attr):
        if not attr:
            raise ValidationError('确认密码不能为空!')
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        old_password = attrs.get('old_password')
        user_obj = auth.authenticate(username=username, password=old_password)
        if user_obj:
            new_password = attrs.get('new_password')
            confirm_password = attrs.get('confirm_password')
            if new_password == confirm_password:
                if not new_password == old_password:
                    return attrs
                raise ValidationError('新密码不能与原密码重复')
            raise ValidationError('两次密码不一致')
        raise ValidationError('原密码错误')

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance


# SetAvatarView

class SetAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserInfo
        fields = ['avatar']

    def update(self, instance, validated_data):
        file_obj = validated_data.get('avatar')
        if file_obj:
            instance.avatar = file_obj
        else:
            instance.avatar = 'avatar/w.jpg'
        instance.save()
        return instance


# BackendCreatedView

class BackendCreatedSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='blog.site_name')

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'up_num', 'comment_num', 'site_name']


# UpOrDownView

class UpOrDownSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True)
    is_up = serializers.BooleanField()

    class Meta:
        model = models.Article
        fields = ['username', 'is_up']

    def validate_username(self, attr):
        if not attr:
            raise ValidationError('<a href="/login">请先登录</a>')
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        user = models.UserInfo.objects.filter(username=username).first()
        if not self.instance.blog == user.blog:
            is_click = models.UpAndDown.objects.filter(user=user, article=self.instance)
            if not is_click:
                attrs['user'] = user
                return attrs
            raise ValidationError('不能重复点击')
        raise ValidationError('自己不能点击')

    def update(self, instance, validated_data):
        user = validated_data.get('user')
        is_up = validated_data.get('is_up')
        if is_up:
            instance.up_num += 1
            self.context['msg'] = '点赞成功'
        else:
            instance.down_num += 1
            self.context['msg'] = '点踩成功'
        models.UpAndDown.objects.create(user=user, article=instance, is_up=is_up)
        instance.save()
        return instance


# CommentView

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True)
    article_id = serializers.CharField()
    parent_id = serializers.CharField(allow_blank=True)

    class Meta:
        model = models.Comment
        fields = ['username', 'article_id', 'content', 'parent_id']

    def validate(self, attrs):
        username = attrs.get('username')
        if username:
            user = models.UserInfo.objects.filter(username=username).first()
            attrs.pop('username')
            attrs['user'] = user
            return attrs
        raise ValidationError({'comment_error': '<a href="/login">请先登录</a>'})

    def create(self, validated_data):
        article_id = validated_data.get('article_id')
        with transaction.atomic():
            models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
            user_obj = models.Comment.objects.create(**validated_data)
        content_time = user_obj.content_time
        self.context['msg'] = content_time.strftime('%Y-%m-%d %H:%M:%S')
        return user_obj


# VipView

class VipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserInfo
        fields = ['username']

    def validate(self, attrs):
        if not self.instance.is_staff:
            return attrs
        raise ValidationError('不能重复购买')

    def update(self, instance, validated_data):
        instance.is_staff = True
        instance.save()
        return instance


# AddArticleCreatedView

class AddArticleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ['id', 'name']


class AddArticleTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ['id', 'name']


class AddArticleCreatedSerializer(serializers.ModelSerializer):
    category_list = AddArticleCategorySerializer(many=True, source='category_set')
    tag_list = AddArticleTagSerializer(many=True, source='tag_set')

    class Meta:
        model = models.Blog
        fields = ['category_list', 'tag_list']


# UploadImageView

class UploadImageSerializer(serializers.ModelSerializer):
    imgFile = serializers.FileField()

    class Meta:
        model = models.Article
        fields = ['imgFile']

    def validate(self, attrs):
        file_obj = attrs.get('imgFile')
        file_dir = os.path.join(settings.BASE_DIR, 'media', 'article_img')
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        file_path = os.path.join(file_dir, file_obj.name)
        with open(file_path, mode='wb') as w:
            for w1 in file_obj:
                w.write(w1)
        self.context['url'] = '/media/article_img/%s' % file_obj.name
        return attrs


# AddArticleView

class AddArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    tag = serializers.ListField(write_only=True)

    class Meta:
        model = models.Article
        fields = ['username', 'title', 'content', 'category', 'tag']

    def validate_content(self, attr):
        soup = BeautifulSoup(attr, 'html.parser')
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        return attr

    def validate(self, attrs):
        username = attrs.get('username')
        content = attrs.get('content')
        user = models.UserInfo.objects.filter(username=username).first()
        soup = BeautifulSoup(content, 'html.parser')
        desc = soup.text[0:130]
        attrs.pop('username')
        attrs['content'] = str(soup)
        attrs['desc'] = desc
        attrs['blog'] = user.blog
        return attrs

    def create(self, validated_data):
        tag_id_list = validated_data.get('tag')
        validated_data.pop('tag')
        article_obj = models.Article.objects.create(**validated_data)
        article_obj_list = []
        for tag_id in tag_id_list:
            tag_article_obj = models.Article2Tag(article=article_obj, tag_id=tag_id)
            article_obj_list.append(tag_article_obj)
        models.Article2Tag.objects.bulk_create(article_obj_list)
        return article_obj