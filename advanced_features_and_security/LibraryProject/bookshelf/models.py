from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The Email field must be set')
		
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self.create_user(email, password, **extra_fields)
		
class CustomUser(AbstractUser):
	date_of_birth = models.DateField(
		null=True,
		blank=True,
		help_text="User's date of birth"
	)
	
	profile_photo = models.ImageField(
		upload_to='profile_photos.',
		null=True,
		blank=True,
		help_text="User's profile photo"
	)
	
	objects = CustomUserManager()
	
	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'
		
	def __str__(self):
		return self.username
	
	def get_full_name(self):
		return f"{self.first_name} {self.last_name}".strip() or self.username
		
	def get_age(self):
		if self.date_of_birth:
			from datetime import date
			today = date.today()
			return today.year - self.date_of_birth.year - (
				(today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
			)
			return None

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=100)
	publication_year = models.IntegerField()
	
	class Meta:
		permissions = [
			("can_view", "Can view book"),
			("can_create", "Can create book"),
			("can_edit", "Can edit book"),
			("can_delete", "Can delete book"),
		]

	def __str__(self):
		return self.title
