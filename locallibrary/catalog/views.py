from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):
    """View function for home page of the site"""

    page_name = "Home Page"

    num_books = Book.objects.all().count()

    num_instances = BookInstance.objects.all().count()

    instances_available = BookInstance.objects.filter(status__exact='a')
    num_instances_available = instances_available.count()

    num_novels = Book.objects.filter(genre__name__icontains='novel').count()

    num_authors = Author.objects.all().count()

    context = {
        'page_name': page_name,
        'num_books': num_books,
        'num_novels': num_novels,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    model = Book

    context_object_name = 'book_list'

    # queryset = Book.objects.filter(title__icontains='picture')[:5]

    template_name = 'catalog/book_list.html'

    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book

    template_name = 'catalog/book_detail.html'
