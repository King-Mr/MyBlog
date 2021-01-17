from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from Blog.models import Post,Category,Tag
from Config.models import Link,SideBar
from Comment.forms import CommentForm
from Comment.models import Comment
from django.views.generic import ListView,DetailView
from django.db.models import Q
from MyBlog.package.base import MEDIA_ROOT
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

#提供get_context_data的一个基类，它的子类会同时继承与其他有get_context_data的类
#context = super().get_context_data(**kwargs)这就是调用它子类的父类的这个方法，用来获取源数据
#获取到源数据之后，在本类中添加页面中需要获得的其他数据，比如侧边栏，类别数据
#get_context_data这个方法主要提供渲染到模板的数据
class CommonViewMixin():
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)#获取文章数据，page数据
        context.update(                             #添加侧边栏数据
            {'sidebars':SideBar.get_all()}
        )
        context.update(                             #添加类别数据
            Category.get_navs()
        )
        return context

#多重继承的父类顺序决定了引用属性或函数搜索的顺序
#比如两个父类都定义了get_context_data，调用这个函数的时候就会先从第一个父类中搜索，再去搜索第二个父类
#如果继承的顺序是(ListView，CommonViewMixin)，那么调用的时候就会调用ListView的get_context_data函数。而不会调用第二个父类。
class IndexView(CommonViewMixin,ListView):#首页
    queryset = Post.latest_posts()
    context_object_name = 'post_list'
    template_name = 'Template/default/Blog/list.html'






class CategoryView(IndexView):  #分类页面
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update(
            {'category':category}
        )
        return context
    def get_queryset(self):#这个函数获取当前页面需要的数据，并且过滤掉不需要的数据
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)



class TagView(IndexView):   #标签过滤页面
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update(
            {'tag':tag}
        )
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')#在Urls链接里设置了参数才能用这种方式获取
        return queryset.filter(tag_id=tag_id)


#DetailView类中的get_object函数会通过url中的参数直接在querryset中获取对象，所以就不需要再配置queryset中过滤对象
class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'Template/new_style/Blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        comment_list = Comment.get_by_target(self.request.path)
        count = comment_list.count()
        context.update({
            'comment_form':CommentForm,
            'comment_list':comment_list,
        })
        print(context)
        return context



class OwnerView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.kwargs.get('user_id')#在Urls链接里设置了参数才能用这种方式获取
        return queryset.filter(owner_id=user_id)

class SearchView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        search_key = self.request.GET.get('search_key')#urls文件中链接里没设置参数，按钮提交的键值需要这样获取
        print(search_key)
        return queryset.filter(Q(title__icontains=search_key) | Q(desc__icontains=search_key))



