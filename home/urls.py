from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', ListPage.as_view(), name='member-list'),
    path('add/', AddPage.as_view(), name='member-add'),
    path('edit/<int:memberId>', EditPage.as_view(), name='member-edit'),
    path('delete/<int:pk>/', DeleteView.as_view(), name='member-delete'),
]