from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from Blog.models import Post,Category,Tag
from Config.models import Link,SideBar
from Comment.models import Comment
from django.views.generic import ListView,DetailView
from MyBlog.package.base import *
# Create your views here.

'''
def post_list(request,category_id=None,tag_id=None):
    tag=None
    category = None
    if tag_id:
        post_list,tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list,category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context ={
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request,'Template/Blog/list.html',context=context)




def post_detail(request,post_id=None):
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post':post,
    }
    context.update(Category.get_navs())
    return render(request,'Template/Blog/detail.html',context=context)'''


class CommonViewMixin():
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'sidebars':SideBar.get_all()}
        )
        context.update(
            Category.get_navs()
        )
        return context

#多重继承的父类顺序决定了引用属性或函数搜索的顺序
#比如两个父类都定义了get_context_data，调用这个函数的时候就会先从第一个父类中搜索，再去搜索第二个父类
#如果继承的顺序是(ListView，CommonViewMixin)，那么调用的时候就会调用ListView的get_context_data函数。而不会调用第二个父类。
class IndexView(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'Template/default/Blog/list.html'
    print(TEMPLATES)





class CategoryView(IndexView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update(
            {'category':category}
        )
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)



class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update(
            {'tag':tag}
        )
        return context


class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'Template/default/Blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'