from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Library
from .models import Book

def list_books(request):
	books = Book.objects.all()
	context = {
		'books': books
	}
	return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
	model = Library
	template_name = 'relationship_app/library_detail.html'
	context_object_name = 'library'
