from django import forms
from repository import models
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = models.Article
        # fields = ['title', 'summary']
        fields = '__all__'
        exclude = ['read_count', 'comment_count', 'up_count', 'down_count', 'blog']
        labels = {
            'title': '标题',
            'summary': '简介',
        }
        widgets = {
            'title': Fwidgets.Input(attrs={'class': "form-control", 'id': "title", 'placeholder': "文章标题"}),
            'summary': Fwidgets.Textarea(attrs={'class': "form-control", 'placeholder': "文章简介"})
        }
        error_messages = {
            '__all__': {

            },
            'title': {
                'required': '标题不能为空',
            },
            'summary': {
                'required': '简介不能为空',
            }
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_summary(self):
        summary = self.cleaned_data['summary']
        return summary


class ArticleDetailModelForm(forms.ModelForm):
    class Meta:
        model = models.ArticleDetail
        # fields = ['content']
        fields = ['content']
        exclude = ['article']
        labels = {
            'content': '内容',
        }
        widgets = {
            'content': Fwidgets.Textarea(attrs={'class': 'content_css', 'name': "content"})
        }
        error_messages = {
            '__all__': {

            },
            'content': {
                'required': '内容不能为空',
            }
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        return content
