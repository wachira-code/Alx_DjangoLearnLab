from django import forms
from django.contrib.auth.models import User
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
