from rest_framework import serializers
from ..models import Category
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']

    @extend_schema_field(str)
    def get_children(self, obj):
        return CategorySerializer(obj.get_children(), many=True).data
