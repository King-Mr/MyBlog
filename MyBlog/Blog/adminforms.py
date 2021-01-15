from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class PostAdminForm(forms.ModelForm):
    #desc = forms.CharField(widget=forms.Textarea,label='摘要',required=False)
    #配置富文本编辑器会报错，原因是插件与Django不同步，需要把报错的render参数注释掉
    content = forms.CharField(widget=CKEditorUploadingWidget(),label='正文',required=True)