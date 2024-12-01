from django import forms
from .models import CustomUser, Book, IssuedBook

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
        return cleaned_data

class LoginForm(forms.Form):
    username_or_phone = forms.CharField(max_length=100, label="Username or Phone Number")
    password = forms.CharField(widget=forms.PasswordInput())

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'cover_image', 'is_available', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter author name'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['user', 'phone_number', 'book', 'issue_date']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter user name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter phone number'}),
            'book': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['returned_on']
        widgets = {
            'returned_on': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }