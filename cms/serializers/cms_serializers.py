from rest_framework import serializers
from cms.models.cms import Cms

class CmsSerializers(serializers.ModelSerializer):
    content = serializers.JSONField()

    class Meta:
        model = Cms
        fields = ['id', 'slug', 'content']
