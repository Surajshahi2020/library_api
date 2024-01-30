from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.role = "SU"
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    MembershipDate = models.DateField()
    USERNAME_FIELD = "Email"
    REQUIRED_FIELDS = []

    @property
    def id(self):
        return self.UserID

    def __str__(self) -> str:
        return f"User id:{self.UserID}.{self.Name}"

class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=20, unique=True)
    PublishedDate = models.DateField(null=True, blank=True)
    Genre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"Book id:{self.BookID}.{self.Title}"

class BookDetails(models.Model):
    DetailsID = models.AutoField(primary_key=True)
    Book = models.OneToOneField(Book, on_delete=models.CASCADE)
    NumberOfPages = models.IntegerField()
    Publisher = models.CharField(max_length=255)
    Language = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.DetailsID}.{self.Book} has {self.NumberOfPages} pages written in {self.Language}"

class BorrowedBooks(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    BorrowDate = models.DateField()
    ReturnDate = models.DateField(null=True, blank=True)
    def __str__(self):
        if self.ReturnDate:
            return f"{self.User} borrowed {self.Book} on {self.BorrowDate} and returned on {self.ReturnDate}"
        else:
            return f"{self.User} borrowed {self.Book} on {self.BorrowDate}, not returned"

    class Meta:
        unique_together = ('User', 'Book') 

