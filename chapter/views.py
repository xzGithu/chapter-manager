# coding:utf-8
from django.shortcuts import render,get_object_or_404
from chapter.models import Post,Comment
from taggit.models import Tag
from django.core.paginator import Page,PageNotAnInteger,Paginator,EmptyPage
from django.views.generic import ListView
from chapter.forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.db.models import Count
# Create your views here.


class PostViews(ListView):
    queryset=Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'
def post_list(request,tag_slug=None):
    # posts = Post.published.all()
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug = tag_slug)
        object_list = Post.published.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/list.html',{"page":page,"posts":posts,"tag":tag,})

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.postcomments.filter(actime=True)
    new_comment = None
    if request.method == 'POST':
        commform = CommentForm(request.POST)
        if commform.is_valid():
            new_comment = commform.save(commit=False)
            new_comment.post = post#设置当前评论归属
            new_comment.save()
    else:
        commform = CommentForm()
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_tag_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_tag_post = similar_tag_post.annotate(same_tags=Count('tags')).order_by('-same_tags'
                                                                                   ,'-publish'
                                                                                   )[:4]

    return render(request,'blog/detail.html',{"post":post,
                                              "forms":commform,
                                              "comments":comments,
                                              "new_comment":new_comment,
                                              "similar_tag_post":similar_tag_post,
                                              })

def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}  recommends you to read the chapter  "{}" '.format(cd['name'],post.title)
            message = 'Read "{}" at {} \n,comments {}'.format(post.title,post_url,cd['comments'].encode("utf-8"))
            send_mail(subject,message, 'mistest163@163.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/share.html',{"form":form,"post":post,"sent":sent })







