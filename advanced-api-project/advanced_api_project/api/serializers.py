from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

#serializer for the Book model that includes all the fields
class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ['id', 'title', 'publication_year', 'author']
	
	#Custom validation to ensure the publication year is not in the future	
	def validate_publication_year(self, value):
		current_year = datetime.now().year
		if value > current_year:
			raise serializers.ValidationError(f"Publication year cannot be in the future. Current year is {current_year}.")
		return value

#serializer for the Author model with nested BookSerializer
class AuthorSerializer(serializers.ModelSerializer):
	books = BookSerializer(many=True, read_only=True)
	
	class Meta:
		model = Author
		fields = ['id', 'name', 'books']
