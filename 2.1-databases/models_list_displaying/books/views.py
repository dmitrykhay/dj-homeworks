from datetime import datetime
from django.shortcuts import render
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_date_view(request, slug):
    template = 'books/books_date.html'
    books_date = Book.objects.filter(pub_date=slug)
    list_date_all_books = [book.pub_date for book in Book.objects.all()]
    list_date_all_books.sort()
    date_obj = datetime.strptime(slug, '%Y-%m-%d').date()
    if list_date_all_books.index(date_obj) != 0:
        prev = max(el for el in list_date_all_books if el < date_obj)
    else:
        prev = None
    if list_date_all_books.index(date_obj) != len(list_date_all_books) - 1:
        next = min(el for el in list_date_all_books if el > date_obj)
    else:
        next = None
    context = {
        'books': books_date,
        'prev': prev.strftime('%Y-%m-%d') if prev else None,
        'next': next.strftime('%Y-%m-%d') if next else None,
    }
    return render(request, template, context)

