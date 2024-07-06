from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


# Create your tests here.

class BooksTestCase(TestCase):
    def test_books_not_found(self):
        response = self.client.get(
            reverse('books:list')
        )
        self.assertContains(response, 'No books found.')

    def test_books_list(self):
        book1 = Book.objects.create(title='Test Book1', description='Test description1', isbn='12365655')
        book2 = Book.objects.create(title='Test Book2', description='Test description2', isbn='12365651')
        book3 = Book.objects.create(title='Test Book3', description='Test description3', isbn='12365653')

        response = self.client.get(reverse('books:list') + '?page_size=2')

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)
        response = self.client.get(reverse('books:list') + '?page=2&page_size=2')
        self.assertContains(response, book3.title)
    def test_books_detail(self):
        book = Book.objects.create(title='Test Book1', description='Test description1', isbn='12365655')
        response = self.client.get(
            reverse('books:detail',
                    kwargs={'id': book.id}
                    )
        )
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_books_search(self):
        book1 = Book.objects.create(title='Sport', description='Test description1', isbn='12365655')
        book2 = Book.objects.create(title='Programming', description='Test description2', isbn='12365651')
        book3 = Book.objects.create(title='Python', description='Test description3', isbn='12365653')

        response = self.client.get(reverse('books:list') + '?q=Sport')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=Programming')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=Python')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class ReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Book1', description='Test description1', isbn='12365655')
        self.user = CustomUser.objects.create_user(username='ismoiljon1', first_name='Ismoil', last_name='Mamirov',
                                              email='ismoil@gmail.com')
        self.user.set_password('123456')
        self.user.save()

        self.client.login(username='ismoiljon1', password='123456')

        self.client.post(reverse('books:review', kwargs={'id': self.book.id}), data={
            'rate': 3,
            'comment': 'Test comment',
        })

    def test_add_review(self):
        book_reviews = self.book.reviews.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Test comment')
        self.assertEqual(book_reviews[0].book, self.book)
        self.assertEqual(book_reviews[0].user, self.user)

    def test_edit_review(self):
        review = self.book.reviews.all()[0]
        response = self.client.post(reverse('books:edit-review',
                        kwargs={'book_id': self.book.id, 'review_id': review.id}), data={
            'rate': 5,
            'comment': 'Awesome comment',
        })

        review.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('books:detail', kwargs={'id':self.book.id}))
        self.assertEqual(review.stars_given, 5)
        self.assertEqual(review.comment, 'Awesome comment')

    def test_delete_review(self):
        review = self.book.reviews.all()[0]

        response = self.client.get(reverse('books:delete-review',
                        kwargs={'book_id': self.book.id,
                                'review_id': review.id}))


        review = self.book.reviews.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('books:detail', kwargs={'id':self.book.id}))
        self.assertEqual(review.exists(), False)

