from rest_framework import serializers
from . import models
from .base.services import delete_old_file

class FilmworkSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Filmwork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'certificate',
            'file_path',
            'rating',
            'type',
            'genres'
        )
    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)

class FilmworkDetailSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Filmwork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'certificate',
            'file_path',
            'rating',
            'type',
            'genres'
        )