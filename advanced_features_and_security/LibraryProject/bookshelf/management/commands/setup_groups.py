from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from djanfo.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
	help = 'Set up user groups with appropriate permissions'
	
	def handle(self, *args, **kwargs):
		content_type = ContentType.objects.get_for_model(Book)
		
		can_view = Permission.objects.get(codename='can_view', content_type=content_type)
		can_create = Permission.objects.get(codename='can_create', content_type=content_type)
		can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
		can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)
		
		viewers, created = Group.objects.get_or_create(name='Viewers')
		if created:
			self.stdout.write(self.style.SUCCESS('Created group: Viewers'))
		
		viewers.permissions.set([can_view])
		self.stdout.write(self.style.SUCCESS('✓ Viewers: can_view'))
		
		editors, created = Group.objects.get_or_create(name='Edotors')
		if created:
			self.stdout.write(self.style.SUCCESS('Created Group: Editors'))
		editors.permissions.set([can_view, can_create, can_edit])
		self.stdout.write(self.style.SUCCESS('✓ Editors: can_view, can_create, can_edit'))
		
		admins, created = Group.objects.get_or_create(name='Admins')
		if created:
			self.stdout.write(self.style.SUCCESS('Created Group: Admins'))
		admins.permissions.set([can_view, can_create, can_edit, can_delete])
		self.stdout.write(self.style.SUCCESS('✓ Admins: can_view, can_create, can_edit, can_delete'))
		self.stdout.write(self.style.SUCCESS('\n✅Groups and permissions set up successfully!'))
		self.stdout.write(self.style.WARNING('\nNext steps:'))
		self.stdout.write('1. Go to Django admin: http://127.0.0.1 :8000/admin/')
		self.stdout.write('2. Navigate to Users')
		self.stdout.write('3. Assign users to groups(Viewers, Editors, Admins)')
