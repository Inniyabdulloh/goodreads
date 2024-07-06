from django.http import JsonResponse
from django.views import View
from books.models import Book


# Create your views here.

class BookApiView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        json_data = {
            'book': book.title,
            'description': book.description,
            'isbn': book.isbn,
            'authors': [],
            'comments': []
        }
        authors = book.book_author.all().order_by('-id')
        for author in authors:
            json_data['authors'].append(
                {'id': author.author.id,
                 'first_name':author.author.first_name,
                 'last_name':author.author.last_name}
            )


        reviews = book.reviews.all().order_by('-id')
        for review in reviews:
            json_data['comments'].append(
                {'id': review.id,
                 'user': {
                     'id': review.user.id,
                     'first_name':review.user.first_name,
                     'last_name':review.user.last_name,
                     'username':review.user.username,
                 },
                 'comment': review.comment,
                 'stars_given': review.stars_given,}
            )

        return JsonResponse(json_data)


class BooksListApiView(View):
    def get(self, request):
        books = Book.objects.all().order_by('-id')

        json_data = {
            'books': []
        }

        for book in books:
            book_dict = {
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'isbn': book.isbn,
                'authors': []
               }


            authors = book.book_author.all().order_by('-id')
            for author in authors:
                print(author.author.first_name)
                book_dict['authors'].append(
                    {
                     'id': author.author.id,
                     'first_name': author.author.first_name,
                     'last_name': author.author.last_name
                     }
                )

            json_data['books'].append(book_dict)

        return JsonResponse(json_data)


