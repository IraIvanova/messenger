from django.urls import path
from .views import UsersListPage, EditUserPage

urlpatterns = [
    path('', UsersListPage.as_view(), name='users'),
    path('<int:id>', UsersListPage.as_view(), name='users'),
    path('edit/<int:id>', EditUserPage.as_view(), name='edit_user'),
]
