from . import models
from . import serializer
from w6.utils.response import APIResponse
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView

# Create your views here.


class LoginView(CreateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.LoginSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            username = ser.context['user_obj'].username
            token = ser.context['token']
            return APIResponse(username=username, token=token)
        return APIResponse(code=0, msg=ser.errors)


class RegisterView(CreateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.RegisterSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg="注  册  成  功!")
        return APIResponse(code=0, msg=ser.errors)


class CreatedView(ListAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.CreatedSerializer


class SiteCreatedView(ListAPIView):
    serializer_class = serializer.SiteCreatedSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = models.Article.objects
        category = self.request.query_params.get('category_id')
        tag = self.request.query_params.get('tags__id')

        if category:
            self.filter_fields = ['blog__site_name', 'category_id']
        elif tag:
            self.filter_fields = ['blog__site_name', 'tags__id']
        else:
            self.filter_fields = ['blog__site_name']
        return queryset


class ArticleDetailCreatedView(ListAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.ArticleDetailCreatedSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['blog__site_name', 'id']


class SearchView(ListAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.CreatedSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']


class SetPasswordView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.SetPasswordSerializer
    lookup_field = 'username'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance=instance, data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg="修改成功")
        return APIResponse(code=0, msg=ser.errors)


class SetAvatarView(RetrieveUpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.SetAvatarSerializer
    lookup_field = 'username'


class BackendCreatedView(ListAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.BackendCreatedSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['blog__site_name']
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]


class UpOrDownView(UpdateAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.UpOrDownSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance=instance, data=request.data)
        if ser.is_valid():
            ser.save()
            msg = ser.context['msg']
            return APIResponse(msg=msg)
        return APIResponse(code=0, msg=ser.errors)


class CommentView(CreateAPIView):
    queryset = models.Comment.objects
    serializer_class = serializer.CommentSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            msg = ser.context['msg']
            return APIResponse(msg=msg)
        return APIResponse(code=0, msg=ser.errors)


class VipView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = serializer.VipSerializer
    lookup_field = 'username'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = self.get_serializer(instance=instance, data=request.data)
        if ser.is_valid():
            ser.save()
            return APIResponse(msg='支付成功')
        return APIResponse(code=0, msg=ser.errors)


class AddArticleCreatedView(RetrieveAPIView):
    queryset = models.Blog.objects
    serializer_class = serializer.AddArticleCreatedSerializer
    lookup_field = 'site_name'
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]


class UploadImageView(CreateAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.UploadImageSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            url = ser.context['url']
            return APIResponse(url=url)
        return APIResponse(code=0, msg=ser.errors)


class AddArticleView(CreateAPIView):
    queryset = models.Article.objects
    serializer_class = serializer.AddArticleSerializer