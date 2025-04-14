from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db.models import Q
from django.core.paginator import Paginator



def book_list(request):
    query = request.GET.get('q')
    sort_order = request.GET.get('sort', 'newest')  # ✅ GET the sort order from URL

    books = Book.objects.all()

    # ✅ Apply search filter if there's a query
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    # ✅ Apply sorting here
    if sort_order == 'oldest':
        books = books.order_by('published_date')
    else:
        books = books.order_by('-published_date')

    # ✅ Pagination comes after filtering + sorting
    paginator = Paginator(books, 6)
    page = request.GET.get('page')
    books = paginator.get_page(page)

    return render(request, 'book_list.html', {
        'books': books
    })


    




def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})
