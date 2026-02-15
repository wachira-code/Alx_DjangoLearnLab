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

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = modelss.ForeignKey(User, on_delete=models.CASCADE, related_name='comments'
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ['created_at']
		
	def __str__(self):
		return f'Comment by {self.author.username} on {self.post.title}'
		
	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.post.pk}
		
		
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	bio = models.TextField(blank=True)
	
	def __str__(self):
		return f'{self.user.username} Profile'
