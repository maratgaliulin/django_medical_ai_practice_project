from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from mptt.models import TreeForeignKey
from django.urls import reverse

class PostModel(models.Model):
    """Модель поста"""

    class Status(models.TextChoices):
        """Класс выбора статуса поста"""
        DRAFT = 'ЧЕ', 'Черновик'
        PUBLISHED = 'ОП', 'Опубликовано'

    title = models.CharField(max_length=200,
                             verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="Альт. заголовок")
    image = models.ImageField(upload_to='post/%Y/%m/%d',
                              default='default/not_found.png',
                              verbose_name='Изображение поста')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post',
                               verbose_name="Автор")
    category = TreeForeignKey('CategoryModel',
                              on_delete=models.PROTECT,
                              related_name='post',
                              verbose_name='Категория')
    short_body = CKEditor5Field(max_length=350,
                                verbose_name="Краткое описание",
                                blank=True)
    full_body = CKEditor5Field(verbose_name='Содержимое поста')
    publish = models.DateTimeField(default=timezone.now,
                                   verbose_name="Опубликовано")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Обновлено")
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name="Статус")
    

    objects = models.Manager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        """Метод получения URL-адреса объекта"""
        return reverse('blog:post_page', args=[int(self.pk), str(self.slug)])

    def get_next_post(self):
        """Метод получения следующего поста"""
        try:
            return self.get_next_by_publish(category=self.category)
        except PostModel.DoesNotExist:
            return None

    def get_previous_post(self):
        """Метод получения предыдущего поста"""
        try:
            return self.get_previous_by_publish(category=self.category)
        except PostModel.DoesNotExist:
            return None

    def __str__(self):
        return self.title