from django.test import TestCase
from django.urls import reverse
from books.models import Book, Review
from users.models import CustomUser


class AllReviewsTestCase(TestCase):
    def test_all_reviews(self):
        book = Book.objects.create(title='Test Book1', description='Test description1', isbn='12365655')
        book.save()

        user = CustomUser.objects.create_user(username='ismoiljon1', first_name='Ismoil', last_name='Mamirov',
                                              email='ismoil@gmail.com')
        user.set_password('123456')
        user.save()
        self.client.login(username='ismoiljon1', password='123456')

        comment1 = Review.objects.create(user=user, book=book, comment='This is a test comment', stars_given=4)
        comment1.save()
        comment2 = Review.objects.create(user=user, book=book, comment='Nice book', stars_given=5)
        comment2.save()
        comment_count = Review.objects.count()
        response = self.client.get(reverse('home_page') + '?page=1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test comment')
        self.assertContains(response, 'Nice book')
        self.assertEqual(comment_count, 2)