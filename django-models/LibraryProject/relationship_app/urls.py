from django.urls import path
from .views import list_books, LibraryDetailView, register
from django.contrib.auth.views.register import LoginView, LogoutView
from . import views

urlpatterns = [
	path('books/', list_books, name='list_books'),
	path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
	path('register/', register, name='register'),
	path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
	path('admin-dashboard/', views.admin_view, name='admin_view'),
	path('librarian-dashboard/', views.librarian_view, name='librarian_view'),
	path('member-dashboard/', views.member_view, name='member_view'),
	path('access-denied/', views.access_denied, name='access_denied'),
]

