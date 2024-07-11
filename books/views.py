from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from books.models import Book, Review
from .forms import BookReviewForm

# Create your views here.
class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        print(search_query)
        if search_query:
            books = books.filter(title__icontains=search_query)
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {'page_obj': page_obj, 'search_query': search_query}
        return render(request, 'books/books-list.html', context)


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        book_author = book.book_author.all()
        review_form = BookReviewForm()
        context = {
            "book": book, "review_form": review_form,
            "book_author": book_author
        }
        return render(request, "books/detail.html", context)


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        stars = request.POST.get('rate')
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            Review.objects.create(
                book=book,
                user=request.user,
                stars_given=stars,
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "books/detail.html", {"book": book, "review_form": review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(pk=review_id)
        if request.user != review.user:
            return redirect(reverse("books:detail", kwargs={"id": book_id}))
        review_form = BookReviewForm(instance=review)
        return render(request, 'books/edit-review.html', {'review_form': review_form})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        # if request.user == review.user:
        stars = request.POST.get('rate')
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            review.stars_given = stars
            review.comment = review_form.cleaned_data['comment']
            review.save()
            return redirect(reverse("books:detail", kwargs={"id": book_id}))

        return render(request, "books/edit-review.html", {"review_form": review_form})


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        if request.user != review.user:
            return redirect(reverse("books:detail", kwargs={"id": book_id}))
        return render(request, 'books/delete-review.html', {'book':book,'review':review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.reviews.get(id=review_id)
        review.delete()
        messages.success(request, "Review deleted successfully")
        return redirect(reverse("books:detail", kwargs={"id": book_id}))



