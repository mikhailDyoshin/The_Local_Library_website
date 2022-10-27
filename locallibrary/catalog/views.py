import datetime
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from catalog.forms import RenewBookForm


def index(request):
    """View function for home page of the site"""

    page_name = "Home Page"

    num_books = Book.objects.all().count()

    num_instances = BookInstance.objects.all().count()

    instances_available = BookInstance.objects.filter(status__exact='a')
    num_instances_available = instances_available.count()

    num_novels = Book.objects.filter(genre__name__icontains='novel').count()

    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'page_name': page_name,
        'num_books': num_books,
        'num_novels': num_novels,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book

    context_object_name = 'book_list'

    # queryset = Book.objects.filter(title__icontains='picture')[:5]

    template_name = 'catalog/book_list.html'

    paginate_by = 10


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

    template_name = 'catalog/book_detail.html'


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author

    context_object_name = 'author_list'

    template_name = 'catalog/author_list.html'

    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

    template_name = 'catalog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        borrowed_books = BookInstance.objects.filter(borrower=self.request.user)
        on_loan_books = borrowed_books.filter(status__exact='o').order_by('due_back')
        return on_loan_books
        

class AllLoanedBooksView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to all users."""
    permission_required = 'catalog.can_display_all_borrowed'

    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        all_borrowed_books = BookInstance.objects.all()
        all_on_loan_books = all_borrowed_books.filter(status__exact='o').order_by('due_back')
        return all_on_loan_books


@login_required
@permission_required('catalog.can_renew', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request the process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Process the data in form.cleaned_data as required
            # and write it to the model due_back field
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(
            initial={'renewal_date': proposed_renewal_date}
        )

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
