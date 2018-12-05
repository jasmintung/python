from django.db import models

# Create your models here.


class Category(models.Model):
    caption = models.CharField(max_length=16)


class Article(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type_choice = (  # 保存在内存中的字段,不用重新更新数据库,直接修改后,前端可直接访问
        (1, 'python'),
        (2, 'OpenStack'),
        (3, 'Linux'),
        (4, 'Go'),
    )
    article_type_id = models.IntegerField(choices=type_choice)
