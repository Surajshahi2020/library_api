from rest_framework import serializers
from datetime import datetime
from apis.models import (
    User,
    Book,
    BookDetails,
    BorrowedBooks,
)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "UserID",
            "Name",
            "Email",
            "MembershipDate",
        ]

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "BookID",
            "Title",
            "ISBN",
            "PublishedDate",
            "Genre",
        ]     

class BookDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetails
        fields = [
            'NumberOfPages',
            'Publisher',
            'Language'
        ]  

class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = [
            'id',
            'User',
            'Book',
            'BorrowDate'
        ]
    def create(self, validated_data):
        borrow_date = validated_data.get('BorrowDate')
        borrowed_book_data = {
            'User': validated_data['User'],
            'Book': validated_data['Book'],
            'BorrowDate': borrow_date,
            'ReturnDate': None,  
        }
        borrowed_book = BorrowedBooks.objects.create(**borrowed_book_data)
        return borrowed_book

class BorrowBookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = [
            'id',
            'ReturnDate',
        ]







