from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .views import APIView
from rest_framework.response import Response
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
		serializer.save(author=self.request.user)
		
class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-created_at')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
	pagination_class = PostPagination
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class FeedView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self, request):
		following_users = request.user.following.all() #get all users that current user follows
		posts = Post.objects.filter(author__in=following_users).order_by('-created_at') #get posts from those users with the most recent coming first
		paginator = PostPagination()
		paginated_posts = paginator.paginate_queryset(posts, request)
		serializer = PostSerializer(paginated_posts, many=True)
		return Paginator.get_paginated_response(serializer.data)
