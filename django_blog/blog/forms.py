from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
	
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
		
	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
		
class UserUpdateForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']
		
class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'content']
		widgets = {
			'title': forms.TextInput(attrs={
				'class': 'form-control',
				'placeholder': 'Write your post content here...',
				'rows': 10
			}),
			'content': forms.Textarea(attres={
				'class': 'form-control',
				'placeholder': 'Write your post content here',
				'rows': 10
			}),
			'tags': TagWidget(attrs={
				'class': 'form-control',
				'placeholder': 'Enter tags separated by commas'
			}),
		labels = {
			'title': 'Post Title',
			'content': 'Post Content',
			'tags': 'Tags'
		}
		help_texts = {
			'tags': 'Separate multiple tags with commas'
		}
		
		
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['title'].label = 'Post Title'
			self.fields['content'].label = 'Post Content'

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
		widgets = {
			'content': forms.Textarea(attrs={
				'class': 'form-control',
				'placeholder': 'Write your comment here...',
				'rows': 4
			}),
		}
		labels = {
			'content': 'Your Comment'
		}
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['content'].required = True		
