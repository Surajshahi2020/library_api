from django.urls import path, include
from rest_framework import routers
from apis.viewsets.user import (
    UserViewSet,
    BookViewSet,
    BookDetailViewSet,
    BorrowBookViewSet,
    )

router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user_viewset")
router.register("book", BookViewSet, basename="book_viewset")
router.register("book-details", BookDetailViewSet, basename="book_viewset")
router.register("borrow-book", BorrowBookViewSet, basename="borrowbook_viewset")

urlpatterns = [
    path("", include(router.urls)),
]