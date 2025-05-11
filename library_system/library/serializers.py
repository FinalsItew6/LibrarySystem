from rest_framework import serializers
from .models import Book, BorrowTransaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowTransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)  # ✅ this line

    class Meta:
        model = BorrowTransaction
        fields = [
            'id',
            'user',
            'user_name',
            'book',
            'book_title',  
            'borrow_date',
            'return_date',
            'status'
        ]
