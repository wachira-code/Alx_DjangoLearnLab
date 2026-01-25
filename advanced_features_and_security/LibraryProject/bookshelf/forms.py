from django import forms
from django.core.exceptions import ValidationError
from .models import Book
import re


class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books
    Django automatically sanitizes input and prevents XSS
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year'
            }),
        }
    
    def clean_title(self):
        """
        Custom validation for title field
        """
        title = self.cleaned_data.get('title')
        
        # Remove leading/trailing whitespace
        title = title.strip()
        
        # Ensure title is not empty after stripping
        if not title:
            raise ValidationError('Title cannot be empty or only whitespace.')
        
        # Check for minimum length
        if len(title) < 2:
            raise ValidationError('Title must be at least 2 characters long.')
        
        return title
    
    def clean_author(self):
        """
        Custom validation for author field
        """
        author = self.cleaned_data.get('author')
        
        # Remove leading/trailing whitespace
        author = author.strip()
        
        # Ensure author is not empty
        if not author:
            raise ValidationError('Author name cannot be empty.')
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[A-Za-z\s\-'\.]+$", author):
            raise ValidationError('Author name contains invalid characters.')
        
        return author
    
    def clean_publication_year(self):
        """
        Custom validation for publication year
        """
        year = self.cleaned_data.get('publication_year')
        
        # Validate year range
        current_year = 2025
        if year < 1000 or year > current_year:
            raise ValidationError(
                f'Publication year must be between 1000 and {current_year}.'
            )
        
        return year


class BookSearchForm(forms.Form):
    """
    Secure search form - validates and sanitizes search queries
    """
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books by title or author...',
            'aria-label': 'Search'
        })
    )
    
    def clean_query(self):
        """
        Sanitize search query
        """
        query = self.cleaned_data.get('query', '')
        
        # Remove leading/trailing whitespace
        query = query.strip()
        
        # Limit length
        if len(query) > 200:
            query = query[:200]
        
        return query


class ExampleForm(forms.Form):
    """
    Example form demonstrating comprehensive validation
    """
    name = forms.CharField(
        max_length=100,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message',
            'rows': 5
        })
    )
    
    def clean_name(self):
        """Validate and sanitize name"""
        name = self.cleaned_data.get('name')
        name = name.strip()
        
        # Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[A-Za-z\s\-']+$", name):
            raise ValidationError('Name can only contain letters, spaces, hyphens, and apostrophes.')
        
        return name
    
    def clean_message(self):
        """Validate message content"""
        message = self.cleaned_data.get('message')
        message = message.strip()
        
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')
        
        return message
