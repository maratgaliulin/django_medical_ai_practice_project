from rest_framework import serializers

from . import models


class FileModelSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField()
    post_url = serializers.SerializerMethodField()


    class Meta:
        model = models.PostFilesModel
        fields = ['title', 'file_path', 'post_url']

    @staticmethod
    def get_file_path(obj):
        return obj.file.path if obj.file else None
    
    @staticmethod
    def get_post_url(obj: models.PostFilesModel):
        try:
            url = obj.post.get_absolute_url()
            return get_current_site(None).domain + url
        except ObjectDoesNotExist:
            return None