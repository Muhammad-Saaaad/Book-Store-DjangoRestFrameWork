from rest_framework import serializers

from .models import *
from authentication.serializer import *

class ShopSerializerShow(serializers.ModelSerializer):
    user = RegisterSerializer()
    class Meta:
        model = Shop
        fields= '__all__'

class ShopSerializerInsert(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class BookSerializerInsert(serializers.ModelSerializer):
    class Meta:
        model= Book
        fields= '__all__'

class BookSerializerGetDelete(serializers.ModelSerializer):
    # shop = ShopSerializerShow()
    class Meta:
        model= Book
        exclude = ['user']
        depth = 1
