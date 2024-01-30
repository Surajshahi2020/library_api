from django.contrib import admin
from apis.models import (
    User,
    Book,
    BookDetails,
    BorrowedBooks,
)
# Register your models here.
admin.site.register([User,Book,BookDetails,BorrowedBooks])
