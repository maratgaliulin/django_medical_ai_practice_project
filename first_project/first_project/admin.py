from django.contrib import admin
from . import models
from django.utils.html import format_html


@admin.register(models.PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'author', 'category', 'publish', 'created',
                    'updated', 'status', ]
    list_filter = ['status', 'publish', 'author', ]
    search_fields = ['title', 'body', ]
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish', ]
    exclude = ["author", ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
        super().save_model(request, obj, form, change)

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100"/>')
        else:
            return '(No image found)'

    image_preview.short_description = 'Превью'


@admin.register(models.PostFilesModel)
class PostFilesAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'download_count', )
    search_fields = ['title', ]
    exclude = ['download_count', ]
    readonly_fields = ('code',)
    