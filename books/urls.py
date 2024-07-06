from django.urls import path
from .views import BooksView, BookDetailView, AddReviewView, EditReviewView, DeleteReviewView

app_name = 'books'
urlpatterns = [
    path('', BooksView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='review'),
    path('<int:book_id>/review/<int:review_id>/edit/', EditReviewView.as_view(), name='edit-review'),
    path('<int:book_id>/review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review'),
]