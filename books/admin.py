from django.contrib import admin
from books.models import Book, BookAuthor, Author, Review
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    list_display = ('title', 'isbn', 'description')

class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('author', 'title')

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('book', 'author')

admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Review, ReviewAdmin)