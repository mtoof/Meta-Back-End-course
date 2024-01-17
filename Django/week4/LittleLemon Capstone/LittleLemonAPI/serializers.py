from rest_framework import serializers
from .models import MenuItem, Category
from rest_framework.validators import UniqueValidator

class CategorySeralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemsSerializer(serializers.ModelSerializer):
    category = CategorySeralizer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    title = serializers.CharField(max_length=255,
    validators=[UniqueValidator(queryset=MenuItem.objects.all())]
    )
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category', 'category_id']
        depth = 1
