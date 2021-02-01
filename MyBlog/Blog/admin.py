from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from MyBlog.custom_site import custom_site
from MyBlog.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry

from .models import Post,Category
from .adminforms import PostAdminForm
# Register your models here.





@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','owner','created_time')
    fields = ('name','status','is_nav','color')

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'






class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    list_display = ('title','status','created_time','owner','operator')
    list_display_links = ()
    form = PostAdminForm
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category_name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True


    fieldsets = (
        ('基础配置',{'description':'基础配置描述',
                'fields':('title','category',
                'status')
                }),
        ('内容',{'fields':('desc','content',),}),
    )
    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request,obj,form,change)

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:Blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'










@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']
