# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):  #添加新的manager方法
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=10,default="draft")

    objects = models.Manager()
    published = PublishedManager()  #引用新的manager方法
    tags = TaggableManager()

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        # get_absolute_url
        return reverse("chapter:post_detail",args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="postcomments")
    name = models.CharField(max_length=20)
    body = models.TextField(verbose_name="评论内容")
    email = models.EmailField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    actime = models.BooleanField(default=True)

    class Meta:
        ordering = ['create']
    def __str__(self):
        return '{} published comments at {}'.format(self.name,self.create)





