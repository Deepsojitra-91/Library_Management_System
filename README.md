# Library_Management_System

The **Library Management System** is a Django-based web application designed to manage library operations efficiently. It supports user registration, book management, issuing, and returning books. This system simplifies the process of library management with user-friendly interfaces and powerful backend functionality.

---

## Features

### User Management
- **Signup/Login**: Users can register using their email, phone number, and password, or log in with credentials.
- **Custom User Model**: Extended the default Django `AbstractUser` model to include phone numbers and email validation.

### Book Management
- **Add Books**: Admins can add books with attributes such as title, author, category, and cover image.
- **Edit/Delete Books**: Modify or remove book details.
- **Filter Books**: Filter books by availability or category.

### Issue and Return Management
- **Issue Books**: Users can issue available books.
- **Return Books**: Mark issued books as returned and update their availability.
- **Revert Returns**: Undo a return operation if needed.

### Dashboard and Reports
- **Dashboard**: A central place to manage and view library operations.
- **Issued Books**: Track all currently issued books with user details.

---

## Installation

### Prerequisites
1. **Python**: Version 3.8 or later.
2. **MySQL Database**: Ensure MySQL is installed and running.
3. **Django**: Version 4.0 or later.
4. **Virtual Environment**: Recommended for Python package isolation.

### Steps
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd library-management-system
