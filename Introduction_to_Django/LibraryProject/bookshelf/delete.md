from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

all_books = Book.objects.all()
print(f"Total books in database: {all_books.count()}")
print(f"Books: {list(all_books)}")

#Expected Output
(1, {'bookshelf.Book': 1})
Total books in database: 0
Books: []
