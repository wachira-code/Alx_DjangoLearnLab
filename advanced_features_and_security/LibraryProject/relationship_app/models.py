from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

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
			
class Author(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

	def __str__(self):
		return self.title

class Library(models.Model):
	name = models.CharField(max_length=200)
	books = models.ManyToManyField(Book, related_name='libraries')

	def __str__(self):
		return self.name

class Librarian(models.Model):
	name = models.CharField(max_length=200)
	library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

	def __str__(self):
		return self.name
		
class UserProfile(models.Model):
	ROLE_CHOICES = [
		('Admin', 'Admin'),
		('Librarian', 'Librarian'),
		('Member', 'Member'),
	]
	
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
	
	def __str__(self):
		return f"{self.user.username} - {self.role}"
	
	class Meta:
		verbose_name = 'User Profile'
		verbose_name_plural = 'User Profiles'
		
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
