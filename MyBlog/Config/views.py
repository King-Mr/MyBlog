from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def links(request):
    return render(request,'Template/default/Config/list.html',context={'name':'links'})
