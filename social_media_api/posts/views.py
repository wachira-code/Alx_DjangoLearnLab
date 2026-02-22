from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

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

class LikePostView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request, pk):
		post = generics.get_object_or_404(Post, pk=pk)
		like, created = Like.objects.get_or_create(post=post,user=request.user)
		
		if not created:
			return Response({'message': 'You have alraedy liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
			
		if post.author != request.user:
			Notification.objects.create(recipient=post.author, actor=request.user, verb='liked your post', target=post)
			
		return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
		
class UnlikePostView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def post(self, request, pk):
		post = generics.get_object_or_404(Post, pk=pk)
		like = Like.objects.filter(post=post,user=request.user)
		
		if not like.exists():
			return Response({'message': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
			
		like.delete()
		return Response({'message': 'You have unliked this post'}, status=status.HTTP_200_OK)
