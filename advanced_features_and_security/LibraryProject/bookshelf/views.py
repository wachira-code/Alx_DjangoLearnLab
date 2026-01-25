from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm, BookSearchForm, ExampleForm


@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_search(request):
	books = []
	query = ''
	
	if request.method == 'GET':
		form = BookSearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data.get('query', '')
			books = Book.objects.filter(
				Q(title__icontains=query) |
				Q(author__icontains=query)
			)
	else:
		form = BookSearchForm()
	
	context = {
		'form': form,
		'books': books,
		'query': query
	}
	return render(request, 'bookshelf/book_search.html', context)
	
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
	book = get_object_or_404(Book, pk=pk)
	return render(request, 'bookshelf/book+detail.html', {'book': book})
	
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def books_by_author(request, author_name):
	books = Book.objects.filter(author__iexact=author_name)
	context = {
		'books': books,
		'author_name': author_name
	}
	return render(request, 'bookshelf/books_by_author.html', context)
	
	
@login_required
@permission_required('bookshelf.can_create', raise_exception-True)
def book_create(request):
	if request.method == 'POST':
		form = BookForm(request.POST)
		if form.is_valid():
			book = form.save(commit=False)
			book.save()
			messages.success(request, 'Book created successfully!')
			return redirect('book_detail', pk=book.pk)
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = BookForm()
	return render(request, 'bookshelf/book_form.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			form.save()
			messages.success(request, 'Book Updated successfully!')
			return redirect('book_detail', pk=book.pk)
	else:
		form = BookForm(instance=book)
		
	return render(request, 'bookshelf/book_form.html', {
	'book': book
	'form': form
	})
	
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		book_title = book.title
		book.delete()
		messages.success(request, 'Book deleted successfully!')
		return redirect('book_list')
	return render(request, 'bookshelf/book_confirm_delete.html', {'book':book}) 
	
	
