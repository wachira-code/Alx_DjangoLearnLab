from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class PostPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 100
	
class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-created_at')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
	pagination_class = PostPagination
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'content']
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.User)
		
class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-created_at')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
	pagination_class = PostPagination
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.User)
