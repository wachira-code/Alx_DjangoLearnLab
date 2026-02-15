from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(
		required=True,
		widget=forms.EmailInput(attrs={
			'class': 'form-control',
			'placeholder': 'Enter your email'
		})
	)
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		widgets = {
			'username': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Choose a username'
			}),
		}
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Create a password'
		})
		self.fields['password2'].widget.attrs.update({
			'class': 'form-control',
			'placeholder': 'Confirm your password'
		})

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
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated successfully!')
			return redirect('profile')
		else:
			messages.error(request, 'Please correct the errors!')
	else:
		form = UserUpdateForm(instance=request.user)
	
	return render(request, 'blog/profile.html', {'form': form})

def home_view(request):
	return render(request, 'blog/home.html')


#CRUD Operations
class PostListView(ListView):
	model = Post
	template_name = 'blog/post_list.html'
	context_object_name = 'posts'
	paginate_by = 10
	
	def get_Queryset(self):
		return Post.objects.all().select_related('author')
		
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	context_object_name = 'post'
	
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'
	login_url = 'login'
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, 'Post created successfully!')
		return super().form_valid(form)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form_title'] = 'Create new post'
		return context
		
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'
	login_url = 'login'
	
	def form_valid(self, form):
		messages.success(self.request, 'Post updated successfully!')
		return super().form_valid(form)
	
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form_title'] = 'Edit Post'
		return context
		
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'blog/post_confirm_delete.html'
	success_url = reverse_lazy('post_list')
	login_url = 'login'
	
	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
		
	def delete(self, request, *args, **kwargs):
		messages.success(request, 'Post deleted successfully!')
		return super().delete(request, *args, **kwargs)
		

