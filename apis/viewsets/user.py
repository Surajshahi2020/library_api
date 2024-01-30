from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
import datetime
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from django.contrib.auth.models import User
from apis.serializers.user import (
    UserCreateSerializer,
    BookCreateSerializer,
    BookDetailsSerializer,
    BorrowBookSerializer,
    BorrowBookUpdateSerializer,
)
from apis.models import (
    User,
    Book,
    BookDetails,
    BorrowedBooks,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserCreateSerializer
    http_method_names = [
        "post",
        "get",
    ]
    @extend_schema(
        description="New User create Api",
        summary="Create new user",
        responses={
            200: UserCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["User Apis"],
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.filter(UserID=response.data['UserID']).first()
        refresh = RefreshToken.for_user(user)
        refresh.set_exp(lifetime=datetime.timedelta(days=14))
        access = refresh.access_token
        access.set_exp(lifetime=datetime.timedelta(days=1))
        return Response(
            {
                "title": "User",
                "message": "New User created successfully",
                "data": response.data,
                "access": f"{access}",
                "refresh": f"{refresh}",
            }
        )
    
    @extend_schema(
        description="User list Api",
        summary="Retrieve user details",
        responses={
            200: UserCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["User Apis"],
    )
    def list(self, request, *args, **kwargs):
        response =  super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "User",
                "message": "User listed successfully",
                "data": response.data,
            }
        )
    
    @extend_schema(
        description="User Retrieve API",
        summary="Retrieve user details by Id",
        responses={
            200: UserCreateSerializer,
            404: {"description": "User not found"},
        },
        tags=["User Apis"],
    )
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user = get_object_or_404(User, UserID=user_id)
        serializer = UserCreateSerializer(user)
        return Response(
            {
                "title": "User",
                "message": "User retrieved successfully",
                "data": serializer.data,
            },
        )
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter()
    serializer_class = BookCreateSerializer
    http_method_names = [
        "post",
        "get",
    ]
    @extend_schema(
        description="New Book create Api",
        summary="Create new book",
        responses={
            200: BookCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Book Apis"],
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Book",
                "message": "New Book created successfully",
                "data": response.data,
            }
        )
    
    @extend_schema(
        description="Book list Api",
        summary="Retrieve books",
        responses={
            200: UserCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Book Apis"],
    )
    def list(self, request, *args, **kwargs):
        response =  super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Book",
                "message": "Book listed successfully",
                "data": response.data,
            }
        )
    
    @extend_schema(
        description="Book retrieve API",
        summary="Retrieve user details by Id",
        responses={
            200: UserCreateSerializer,
            404: {"description": "User not found"},
        },
        tags=["Book Apis"],
    )
    def retrieve(self, request, *args, **kwargs):
        book_id = kwargs.get("pk")
        book = get_object_or_404(Book, BookID=book_id)
        serializer = BookCreateSerializer(book)
        return Response(
            {
                "title": "Book",
                "message": "Book retrieved successfully",
                "data": serializer.data,
            },
        )



class BookDetailViewSet(viewsets.ModelViewSet):
    queryset = BookDetails.objects.filter()
    serializer_class = BookDetailsSerializer
    http_method_names = [
        "patch",
    ]
    @extend_schema(
        description="Book detail assign Api",
        summary="Book detail assign",
        responses={
            200: BookDetailsSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["Bookdetails Apis"],
    )
    def partial_update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book_details, created = BookDetails.objects.get_or_create(Book=book, defaults=request.data)
        if not created:
            for key, value in request.data.items():
                setattr(book_details, key, value)
            book_details.save()
        serializer = BookDetailsSerializer(book_details)
        return Response(
            {
                "title": "Bookdetails",
                "message": "Bookdetails created/updated successfully",
                "data": serializer.data,
            },
            status=200 if created else 201,
        )
   
class BorrowBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBooks.objects.filter(ReturnDate__isnull=True)
    serializer_class = BorrowBookSerializer
    http_method_names = [
        'post',
        'patch',
        'get',
    ]

    @extend_schema(
        description="Borrow Book API",
        summary="Book Borrow",
        responses={
            200: BorrowBookSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["BorrowBook Apis"],
    )
    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        return Response({
            "title":"Borrowed Book",
            "message":"Book Borrowed successfully",
            "data": response.data,
        })
    
    @extend_schema(
        description="BorrowedBook list Api",
        summary="Borrow books list",
        responses={
            200: UserCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["BorrowBook Apis"],
    )
    def list(self, request, *args, **kwargs):
        response =  super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "BorrowBook",
                "message": "All Borrowed Book listed successfully",
                "data": response.data,
            }
        )
    
    @extend_schema(
        description="BorrowedBook Get by Id Api",
        summary="Borrow books list",
        responses={
            200: UserCreateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["BorrowBook Apis"],
    )
    def retrieve(self, request, *args, **kwargs):
        response =  super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "title": "BorrowBook",
                "message": "All Borrowed Book listed successfully",
                "data": response.data,
            }
        )
    
    @extend_schema(
        description="Borrow Returned API",
        summary="Book Returned update",
        request=BorrowBookUpdateSerializer,
        responses={
            200: BorrowBookUpdateSerializer,
            404: {"message": "Bad Request"},
        },
        tags=["BorrowBook Apis"],
    )
    def partial_update(self, request, pk=None):
        borrow_book = get_object_or_404(BorrowedBooks, pk=pk)
        if borrow_book.ReturnDate is not None:
            return Response(
                {
                    "title": "BorrowBook",
                    "message": "Book has already been returned",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BorrowBookUpdateSerializer(borrow_book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response(
            {
                "title": "BorrowBook",
                "message": "BorrowBook returned successfully",
                "data": serializer.data,
            },
        )