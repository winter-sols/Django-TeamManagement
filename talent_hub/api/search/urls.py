from django.urls import  include, path
from .user.views import (
    SearchUserView
)

urlpatterns = [
    path('users/', SearchUserView.as_view(), name='search_user')
]