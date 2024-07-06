from django.urls import path
from api.views import BookApiView, BooksListApiView
urlpatterns = [
    path('<int:id>/', BookApiView.as_view(), name='book-api'),
    path('books-list/', BooksListApiView.as_view(), name='books-list'),

]