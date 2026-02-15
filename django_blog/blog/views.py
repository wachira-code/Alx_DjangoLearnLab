from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm

def register_view(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request, POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created successfully!')
			return redirect('login')
		else:
			messages.error(request, 'Invalid email or username')
	else:
		form = UserRegistrationForm()
	
	return render(request, 'blog/register.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request, User)
			messages.success(request, f'Welcome back {usernmae}')
			next_page = request.GET.get('next', 'home')
			return redirect(next_page)
		else:
			messages.error(request, 'Invalid username or password.')
	return render(request, 'blog/login.html')
	
def logout_view(request):
	logout(request)
	messages.info(request, 'You have been logged out successfully.')
	return redirect('home')
	
@login_required
def profile_view(request):
	if request.method == 'POST':
		form = UserUpdateForm(request,.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated successfully!')
			return redirect)'profile')
		else:
			messages.error(request, 'Please correct the errors!')
	else:
		form = UserUpdateForm(instance=request.user)
	
	return render(request, 'blog/profile.html', {'form': form})

def home_view(request):
	return render(request, 'blog/home.html.)
	
	
		

