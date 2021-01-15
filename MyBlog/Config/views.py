from django.shortcuts import render
from django.http import HttpResponse
from Blog.views import CommonViewMixin,ListView
from .models import Link
# Create your views here.


class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'Template/default/Config/links.html'
    context_object_name = 'link_list'