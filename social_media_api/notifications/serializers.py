from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
	actor = serializers.StringRelatedField(read_only=True)
	recipient = serializers.StringRelatedField(read_only=True)
	
	class Meta:
		model = Notification
		fields = ['id', 'actor', 'recipient', 'verb', 'timestamp', 'is_read']
