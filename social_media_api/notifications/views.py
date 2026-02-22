from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = NotificationSerializer
	
	def get(self, request):
		notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
		
		unread = notifications.filter(is_read=False)
		unread_count = unread.count()
		unread.update(is_read=True)
		
		serializer = self.get_serializer(notifications, many=True)
		return Response({'unread_count': unread_count, 'notifications': serializer.data})

