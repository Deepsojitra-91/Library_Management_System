from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_books/', views.view_books, name='view_books'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('issue_book/', views.issue_book, name='issue_book'),
    path('view_issued_books/', views.view_issued_books, name='view_issued_books'),
    path('edit-issued-book/<int:pk>/', views.edit_issued_book, name='edit_issued_book'),
    path('delete-issued-book/<int:pk>/', views.delete_issued_book, name='delete_issued_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('revert-return-status/<int:pk>/', views.revert_return_date, name='revert_returned_status'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)