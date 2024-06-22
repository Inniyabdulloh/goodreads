from django.test import TestCase
from django.urls import reverse
from books.models import Book

# Create your tests here.

class BooksTestCase(TestCase):
    def test_books_not_found(self):
        response = self.client.get(
            reverse('books:list')
        )
        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        Book.objects.create(title='Test Book1', description='Test description1', isbn='12365655')
        Book.objects.create(title='Test Book2', description='Test description2', isbn='12365651')
        Book.objects.create(title='Test Book3', description='Test description3', isbn='12365653')

        response = self.client.get(reverse('books:list'))
        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

    def test_books_detail(self):
        book = Book.objects.create(title='Test Book1', description='Test description1', isbn='12365655')
        response = self.client.get(
            reverse('books:detail',
                    kwargs={'id': book.id}
                    )
        )
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
