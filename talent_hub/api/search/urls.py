from django.urls import  include, path
from .user.views import (
    SearchUserView,
    SearchProfileView
)

urlpatterns = [
    path('users/', SearchUserView.as_view(), name='search_user'),
    path('profiles/', SearchProfileView.as_view(), name='search_profile'),
]