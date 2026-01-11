from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")

