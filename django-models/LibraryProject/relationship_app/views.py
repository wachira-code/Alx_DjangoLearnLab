from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.detail import ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Library
from .models import Book
from .models import UserProfile

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
	
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, f'Welcome {user.username}! Your account has been created.')
			return redirect('list_books')
	else:
		form = UserCreationForm()
		
	return render(request, 'relationship_app/register.html', {'form': form})
	
def user_login(request):
	if request.method =='POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f'Welcome back, {username}!')
				return redirect('list_books')
			else:
				messages.error(request, 'Invalid username or password.')
		else:
			messages.error(request, 'Invalid username or password.')
	else:
		form = AuthenticationForm()
		
	return render(request, 'relationship_app/login.html', {'form': form})
	
def user_logout(request):
	logout(request)
	messages.info(request, 'You have been logged out successfully.')
	return redirect('login')

def Admin(user):
	return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def Librarian(user):
	return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'
	
def Member(user):
	return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'
	
@login_required
@user_passes_test(Admin, login_url='/access-denied/')
def admin_view(request):
	return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(Librarian, login_url='/access-denied/')
def librarian_view(request):
	return render(request, 'relationship_app/librarian_view.html')
	
@login_required
@user_passes_test(Member, login_url='/access-denied/')
def member_view(request):
	return render(request, 'relationship_app/member_view.html')

def access_denied(request):
	return render(request, 'relationship_app/access_denied.html', status=404)
