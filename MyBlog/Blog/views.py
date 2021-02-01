from datetime import date
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from Blog.models import Post,Category
from Config.models import Link,SideBar
from Comment.forms import CommentForm
from Comment.models import Comment
from django.views.generic import ListView,DetailView
from django.db.models import Q,F
from MyBlog.package.base import MEDIA_ROOT
from django.core.cache import cache
# Create your views here.


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
        context.update(
            {'friend_links': Link.objects.all()}
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
    template_name = 'Template/new_style/Blog/list.html'






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
        category_id = self.kwargs.get('category_id')
        category = Category.objects.all().get(id=category_id)
        return category.post_set.all().filter(status=1)



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
            'comment_count':count,
        })
        return context

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid,self.request.path)
        uv_key = 'uv"%s:%s:%s' % (uid,str(date.today()),self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key,1,1*60)

        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('uv') + 1)


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



