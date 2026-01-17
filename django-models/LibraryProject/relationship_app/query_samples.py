from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
	author = Author.objects.get(name=author_name)
	books = Book.objects.filter(author=author)

def books_in_library(library_name):
	library = Library.objects.get(name=library_name)
	books = library.books.all()

def librarian_for_library(librarian_name):
	librarian = Librarian.objects.get(name=librarian_name)
	librarian = librarian.librarian
