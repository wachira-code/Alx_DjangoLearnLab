from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book
from datetime import datetime

class BookAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.authenticated_user = User.object.create_user(
			username='testuser'
			password='testpass123'
		)
		self.author1 = Author.objects.create(name='F.K. Bigman')
		self.author2 = Author.objects.create(name='A.S. Rich')
		
		self.book1 = Book.objects.create(
			title='Coming Home',
			publication_year=2000,
			author=self.author1
		)
		self.book2 = Book.objects.create(
			title='Tomorrow Land',
			publication_year=2001,
			author=self.author2
		)
		
		self.list_url = '/api/books/'
		self.create_url = '/api/books/create/'
		
	def test_get_all_books(self):
		response = self.client.get(self.list_url)
		
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 3)
		
	def test_get_single_book(self):
		detail_url = f'/api/books/{self.book1.id}/'
		response = self.client.get(detail.url)
		
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], self.book1.title)
		self.assertEqual(response.data['publication_year'], self.book1.publication_year)
		
	def test_create_book_authenticated(self):
		self.client.force_authenticate(user=self.authenticated_user)
		
		new_book_data = {
			'title': New Book,
			'publication_year': 2002,
			'author': self.Author1.id
		}
		
		response = self.client.post(self.create_url, new_book_data, format='json')
		
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Book.objects.count(), 4)
		self.assertEqual(response.data['title'], 'New Book')
		
	def test_delete_book_authenticated(self):
       
		self.client.force_authenticate(user=self.authenticated_user)
		
		delete_url = f'/api/books/{self.book1.id}/delete/'
		response = self.client.delete(delete_url)
		
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Book.objects.count(), 2)
		self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        
        delete_url = f'/api/books/{self.book1.id}/delete/'
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)  # Book not deleted

    def test_filter_by_author(self):
        
        filter_url = f'{self.list_url}?author={self.author1.id}'
        response = self.client.get(filter_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only Harry Potter books
        for book in response.data:
            self.assertEqual(book['author'], self.author1.id)

    def test_filter_by_publication_year(self):
        
        filter_url = f'{self.list_url}?publication_year=1997'
        response = self.client.get(filter_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)

    def test_search_functionality(self):
        
        search_url = f'{self.list_url}?search=Harry'
        response = self.client.get(search_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Harry Potter books
        
        # Test search by author name
        search_url = f'{self.list_url}?search=Martin'
        response = self.client.get(search_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'A Game of Thrones')

    def test_ordering_by_title(self):
        
        order_url = f'{self.list_url}?ordering=title'
        response = self.client.get(order_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_publication_year_descending(self):
        
        order_url = f'{self.list_url}?ordering=-publication_year'
        response = self.client.get(order_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_combined_filter_search_order(self):
        
        combined_url = f'{self.list_url}?search=Harry&ordering=publication_year'
        response = self.client.get(combined_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify ordering
        self.assertEqual(response.data[0]['publication_year'], 1997)
        self.assertEqual(response.data[1]['publication_year'], 1998)

    def test_invalid_book_id(self):
        
        invalid_url = '/api/books/9999/'
        response = self.client.get(invalid_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_missing_fields(self):
        
        self.client.force_authenticate(user=self.authenticated_user)
        
        incomplete_data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        
        response = self.client.post(self.create_url, incomplete_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
			

