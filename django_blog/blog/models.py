from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	
	class Meta:
		ordering = ['-published_date'] #most recent post
		
	def __str__(self):
		return self.title
		
	def get_absolutr_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})
		
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	bio = models.TextField(blank=True)
	
	def __str__(self):
		return f'{self.user.username} Profile'
