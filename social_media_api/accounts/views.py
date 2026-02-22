from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer

User = get_user_model()

class RegisterView(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny]
	serializer_class = RegisterSerializer
	
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			token, _ = Token.objects.get_or_create(user=user)
			return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class LoginView(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny]
	serializer_class = LoginSerializer
	
	def post(self, request):
		serializer = sself.get_serializer(data=request.data)
		if serializer.is_valid():
			user = authenticate(
				username=serializer.validated_data['username'],
				password=serializer.validated_data['password']
			)
			if user:
				token, _ = token.objects.get_or_create(user=user)
				return Response({'token': token.key})
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class ProfileView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserProfileSerializer
	
	def get(self, request):
		serializer = self.get_serializer(request.user)
		return Response(serializer.data)
		
	def put(self, request):
		serializer = UserProfileSerializer(request.User, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class FollowUserView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get_queryset(self):
		return CustomUser.objects.all()
	
	def post(self, request, user_id):
		target_user = get_object_or_404(CustomUser.objects.all(), pk=user_id)
		
		if target_user == request.user:
			return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
			
		request.user.following.add(target_user)
		return Response({'message': f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)
		
class UnfollowUserView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get_queryset(self):
		return CustomUser.objects.all()
	
	def post(self, request, user_id):
		target_user = get_object_or_404(CustomUser.objects.all(), pk=user_id)
		
		if target_user == request.user:
			return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
			
		request.user.following.remove(target_user)
		return Response({'message': f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)
			

