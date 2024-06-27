from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from books.models import Book, Review
from .forms import BookReviewForm

# Create your views here.
class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
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
        review_form = BookReviewForm()

        return render(request, "books/detail.html", {"book": book, "review_form": review_form})


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