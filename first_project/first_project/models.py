from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import Model, FileField, IntegerField, CharField, TextChoices, SlugField,ImageField, ForeignKey, DateTimeField, Manager, Index, CASCADE, PROTECT
from django.contrib.auth.models import User
from django.utils import timezone 
from mptt.models import TreeForeignKey
from django.urls import reverse


from django.urls import reverse  
from mptt.managers import TreeManager  
from mptt.models import MPTTModel, TreeForeignKey


class CategoryModel(MPTTModel):
    title = CharField(max_length=100,
                             verbose_name="Заголовок")
    slug = SlugField(verbose_name="Альт. заголовок")
    parent = TreeForeignKey('self',
                            on_delete=CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True,
                            verbose_name='Родительская категория')
    description = CharField(max_length=350,
                                   verbose_name="Описание",
                                   blank=True)

    objects = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        app_label = 'first_project'
        unique_together = 'parent', 'slug'
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категории постов'

    def get_absolute_url(self):
        return reverse('blog:category_page', args=[int(self.pk), str(self.slug)])

    def __str__(self):
        return self.title
    

class PostFilesModel(Model):
    title = CharField(max_length=200,
                             verbose_name="Имя файла")
    file = FileField(upload_to='post_files/')
    code = IntegerField(
        default=0,
        verbose_name='Код файла',
        unique=True
    )
    download_count = IntegerField(
        default=0,
        verbose_name='Скачиваний'
    )
    class Meta:
        app_label = 'first_project'
        verbose_name='Файл поста'
        verbose_name_plural = 'Файлы постов'
        

    def increment_download_count(self):
        self.download_count += 1
        self.save()

    def __str__(self):
        return self.title

class PostModel(Model):
    """Модель поста"""

    class Status(TextChoices):
        """Класс выбора статуса поста"""
        DRAFT = 'ЧЕ', 'Черновик'
        PUBLISHED = 'ОП', 'Опубликовано'

    title = CharField(max_length=200,
                             verbose_name="Заголовок")
    slug = SlugField(verbose_name="Альт. заголовок")
    image = ImageField(upload_to='post/%Y/%m/%d',
                              default='default/not_found.png',
                              verbose_name='Изображение поста')
    author = ForeignKey(User,
                               on_delete=CASCADE,
                               related_name='post',
                               verbose_name="Автор")
    category = TreeForeignKey(CategoryModel,
                              on_delete=PROTECT,
                              related_name='post',
                              verbose_name='Категория')
    short_body = CKEditor5Field(max_length=350,
                                verbose_name="Краткое описание",
                                blank=True)
    full_body = CKEditor5Field(verbose_name='Содержимое поста')
    publish = DateTimeField(default=timezone.now,
                                   verbose_name="Опубликовано")
    created = DateTimeField(auto_now_add=True,
                                   verbose_name="Создано")
    updated = DateTimeField(auto_now=True,
                                   verbose_name="Обновлено")
    status = CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name="Статус")
    

    objects = Manager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            Index(fields=['-publish']),
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        app_label = 'first_project'

        

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