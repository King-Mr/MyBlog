"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .custom_site import custom_site
#from Blog.views import post_list,post_detail
from Blog.views import IndexView,CategoryView,TagView,PostDetailView,OwnerView,SearchView
from Config.views import LinkListView
from Comment.views import CommentView
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls,name='super-admin'),
   # path(r'admin/',custom_site.urls,name='admin'),
    path(r'',IndexView.as_view(),name='index'),
    path(r'category/<int:category_id>/',CategoryView.as_view(),name='category-list'),
    path(r'tag/<int:tag_id>/',TagView.as_view(),name='tag-list'),
    path(r'post/<int:post_id>.html',PostDetailView.as_view(),name='post-detail'),
    path(r'links/',LinkListView.as_view(),name='links'),
    path(r'user/<int:user_id>.html',OwnerView.as_view(),name='user-list'),
    path(r'search/',SearchView.as_view(),name='search-list'),
    path(r'comment/',CommentView.as_view(),name='comment'),
    path(r'ckeditor/',include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
