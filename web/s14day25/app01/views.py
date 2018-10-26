from django.shortcuts import render
from app01 import models

# Create your views here.


def article(request, *args, **kwargs):
    print(kwargs)
    condition = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            condition[k] = v
    article_type_list = models.Article.type_choice
    category_list = models.Category.objects.all()
    result = models.Article.objects.filter(**condition)
    return render(
        request,
        'article.html',
        {
            'result': result,
            'article_type_list': article_type_list,
            'category_list': category_list,
            'arg_dict': kwargs
        }
    )