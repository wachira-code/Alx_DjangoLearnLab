#Django Permissions and Groups Setup Guide
#Overview
This implementation uses Django's built-in groups and permissions system to control access to the Book model in the bookshelf app.

#Custom Permissions Defined
The following custom permissions are defined in the Book model:
1. can_view - Can view book
2. can_create = Can create book
3. can_edit - Can edit book
4. can_delete - Can delete book

#Groups and their Permissions
#1. Viewers
Permissions: can_view
Access-level: read-only access to books
Use Case: regular users that can browse the library

#2.Editors
Permissions: can_view, can_create, can_edit
Access-level: can view, add new books and modify existing books
Use Case: content managers, librarians

#3.Admins
Permissions: can_view, can_create, can_edit, can_delete
Access-level: full control over books
Use Case: system administrators


