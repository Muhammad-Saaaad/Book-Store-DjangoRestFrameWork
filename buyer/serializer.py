from rest_framework import serializers

from .models import Buyer
from seller.models import Book

class BooksSerializerShow(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['user']
    
class BooksSerializerBuy(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

    def validate(self, data):
        if 'book_quantity' in data:
            if data['book_quantity']>0:   
                return super().validate(data)
            else:
                raise serializers.ValidationError("quantity cannot be lesser then or equal to zero")
        else:
            raise serializers.ValidationError("Quantity is not available")
    # here we are passing the data back to the original to check for default validation
