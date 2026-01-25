from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Book

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
	books = Book.objects.all()
	return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
	book = get_object_or_404(Book, pk=pk)
	return render(request, 'bookshelf/book_detail.html', {'book': book})
	
@login_required
@permission_required('bookshelf.can_create', raise_exception-True)
def book_create(request):
	if request.method == 'POST':
		messages.success(request, 'Book created successfully!')
		return redirect('book_list')
	return render(request, 'bookshelf/book_form.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		messages.success(request, 'Book Updated successfully!')
		return redirect('book_detail', pk=pk)
	return render(request, 'bookshelf/book_form.html', {'book': book})
	
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
	book = get_object_or_404(Book, pk=pk)
	if request.method == 'POST':
		book.delete()
		messages.success(request, 'Book deleted successfully!')
		return redirect('book_list')
	return render(request, 'bookshelf/book_confirm_delete.html', {'book':book}) 
	
	
