from django.urls import path
from api.views import BookApiView, BooksListApiView, BookListAPIView
urlpatterns = [
    path('<int:id>/', BookApiView.as_view(), name='book-api'),
    path('list/', BookListAPIView.as_view(), name='book-list'),
    path('books-list/', BooksListApiView.as_view(), name='books-list'),

]