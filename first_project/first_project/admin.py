from django.contrib import admin
from . import models


@admin.register(models.PostFilesModel)
class PostFilesAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'download_count', )
    search_fields = ['title', ]
    exclude = ['download_count', ]
    