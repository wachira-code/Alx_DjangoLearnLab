from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
	model = CustomUser
	
	list_display = [
		'username',
		'email',
		'first_name',
		'last_name',
		'date_of_birth',
		'is_staff',
		'is_active'
	]
	
	list_filter = [
		'is_staff',
		'is_superuser',
		'is_active',
		'date_joined'
	]
	
	search_fields = ['username', 'email', 'first_name', 'last_name']
	
	ordering = ['username']
	
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
		('Permissions', {
			'fields': (
				'is_active',
				'is_staff',
				'is_superuser',
				'groups',
				'user_permissions'
			)
		}),
		('Important Dates', {'fields': ('last_login', 'date_joined')}),
	)
	
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields':(
				'username',
				'email',
				'password1',
				'password2',
				'first_name',
				'last_name',
				'date_of_birth',
				'profile_photo',
				'is_staff',
				'is_active'
			),
		}),
	)
	
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(UserProfile)
