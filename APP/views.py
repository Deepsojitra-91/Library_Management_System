from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import CustomUser
from .forms import BookForm, IssueBookForm, ReturnBookForm
from .models import Book, IssuedBook
from django.utils import timezone

# Home page
def home(request):
    return render(request, '1home.html')

def dashboard(request):
    return render(request, '5dashboard.html')

def about(request):
    return render(request, '2about.html')

def signup(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Simple password match check
        if password != confirm_password:
            messages.error(request, "Password and Confirm Password do not match.")
        else:
            # Create the user and save to database
            user = CustomUser(username=username, email=email, phone_number=phone_number, password=password)
            user.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    
    return render(request, '4signup.html')

def login(request):
    if request.method == 'POST':
        username_or_phone = request.POST.get('username_or_phone')
        password = request.POST.get('password')

        user = CustomUser.objects.filter(username=username_or_phone).first() or \
               CustomUser.objects.filter(phone_number=username_or_phone).first()

        if user and user.password == password:
            request.session['username'] = user.username
            messages.success(request, "Login successful!")
            return redirect('view_books')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, '3login.html')

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('view_books')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm()

    return render(request, '7add_book.html', {'form': form})


def view_books(request):
    # Get filters from the request
    availability_filter = request.GET.get('availability', '')
    category_filter = request.GET.get('category', '')

    # Fetch all books
    books = Book.objects.all()

    # Apply filters for availability and category
    if availability_filter == 'available':
        books = books.filter(is_available=True)
    elif availability_filter == 'not_available':
        books = books.filter(is_available=False)

    if category_filter:
        books = books.filter(category=category_filter)

    # Get unique categories from filtered books
    categories = Book.objects.values_list('category', flat=True).distinct()

    return render(request, '6view_books.html', {
        'books': books,
        'availability_filter': availability_filter,
        'category_filter': category_filter,
        'categories': categories,
    })


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('view_books')
    else:
        form = BookForm(instance=book)
    return render(request, '8edit_book.html', {'form': form, 'book': book})

# Delete Book View
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)  # Fetch the book or raise 404 if not found
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('view_books')


def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            issued_book = form.save(commit=False)
            book_id = request.POST.get('book')

            # Get the book being issued
            book = get_object_or_404(Book, id=book_id)

            # Check if the book is available and not already issued
            if book.is_available and not IssuedBook.objects.filter(book=book, returned_on__isnull=True).exists():
                # Set the book as not available
                book.is_available = False
                book.save()

                # Save the issued book
                issued_book.book = book  # Ensure the book field is set properly
                issued_book.save()

                messages.success(request, "Book issued successfully!")
                return redirect('view_issued_books')
            else:
                # If the book is already issued, show an error message
                messages.error(request, "The selected book is not available or is already issued to another user.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IssueBookForm()

    # Get all available books from the database
    available_books = Book.objects.filter(is_available=True)

    return render(request, '9issue_book.html', {'form': form, 'available_books': available_books})



# View issued books page
def view_issued_books(request):
    issued_books = IssuedBook.objects.all()
    return render(request, '10view_issued_books.html', {'issued_books': issued_books})




def edit_issued_book(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)
    if request.method == 'POST':
        form = IssueBookForm(request.POST, instance=issued_book)
        if form.is_valid():
            form.save()
            messages.success(request, "Issued book record updated successfully!")
            return redirect('view_issued_books')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IssueBookForm(instance=issued_book)

    # Ensure the form has the current data and all dropdowns are populated
    available_books = Book.objects.filter(is_available=True)

    return render(request, '11edit_issued_book.html', {
        'form': form,
        'issued_book': issued_book,
        'available_books': available_books
    })

def delete_issued_book(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)
    issued_book.delete()
    messages.success(request, "Book record deleted successfully!")
    return redirect('view_issued_books')


def return_book(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)
    if request.method == 'POST':
        form = ReturnBookForm(request.POST, instance=issued_book)
        if form.is_valid():
            returned_book = form.save(commit=False)
            returned_book.returned_on = form.cleaned_data['returned_on']
            
            # Mark the book as available again
            book = returned_book.book
            book.is_available = True
            book.save()

            returned_book.save()  # Save the updated record with the return date
            messages.success(request, "Book returned successfully!")
            return redirect('view_issued_books')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReturnBookForm(instance=issued_book)

    return render(request, '12return_book.html', {'form': form, 'issued_book': issued_book})


def revert_return_date(request, pk):
    issued_book = get_object_or_404(IssuedBook, pk=pk)

    if request.method == 'POST':
        # Check if there is a returned date set
        if issued_book.returned_on is not None:
            # Clear the returned date to revert the return
            issued_book.returned_on = None

            # Mark the book as not available again
            book = issued_book.book
            book.is_available = False  # Set to False to show the book is not available
            book.save()  # Save the changes to the book

            issued_book.save()  # Save the changes to the issued book
            messages.success(request, "Book return reverted successfully!")
        else:
            messages.error(request, "This book was not marked as returned.")

        return redirect('view_issued_books')

    return render(request, '13revert_return_date.html', {'issued_book': issued_book})