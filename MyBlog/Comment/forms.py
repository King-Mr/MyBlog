from django import forms
from .models import Comment
import mistune

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', max_length=500,
                              widget=forms.widgets.Textarea(attrs={'rows': 6, 'cols': 60,'placeholder':'评论', 'class': 'form-control','style':'resize:none;margin-bottom:40px;'}))
    nickname = forms.CharField(label='',max_length=50,
                            widget=forms.widgets.Input(attrs={'class':'form-control','placeholder':'Name','style':'width:30%;float:left;margin-bottom:40px;'}))
    email = forms.CharField(label='', max_length=50,
                            widget=forms.widgets.EmailInput(attrs={'class': 'form-control','placeholder':'Email', 'style': 'width:30%;float:left;margin-left:calc(5%);margin-bottom:40px;'}))
    website = forms.CharField(label='', max_length=100,
                              widget=forms.widgets.URLInput(attrs={'class': 'form-control','placeholder':'网址', 'style': 'width:30%;float:left;margin-left:calc(5%);margin-bottom:40px;'}))


    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么能这么短呢！！')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['content','nickname','email','website']

