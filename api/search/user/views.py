from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    SearchUserSerializer,
    SearchProfileSerializer,
    SearchPartnerSerializer,
    SearchClientSerializer,
    SearchProjectSerializer
)
from user.models import (
    User,
    Profile
)
from finance.models import (
    Partner,
    Client,
    Project
)

from .filters import UserFilter, ProjectFilter


class SearchUserView(ListAPIView):
    """
    search User by username, first_name, last_name field start with given keyword
    """
    filterset_class = UserFilter
    serializer_class = SearchUserSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['first_name', 'last_name', 'username']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return User.objects.none()
        elif user.is_admin:
            return User.objects.all()
        elif user.is_team_manager:
            return user.team_members

class SearchProfileView(ListAPIView):
    """
    search Profile by first_name, last_name field start with given keyword
    """
    queryset = Profile.objects.all()
    serializer_class = SearchProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']


class SearchPartnerView(ListAPIView):
    """
    search Partner by fullname field start with given keyword
    """
    queryset = Partner.objects.all()
    serializer_class = SearchPartnerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['full_name']


class SearchClientView(ListAPIView):
    """
    search Client by fullname field start with given keyword
    """
    queryset = Client.objects.all()
    serializer_class = SearchClientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['full_name']


class SearchProjectView(ListAPIView):
    """
    search Project by title field start with given keyword
    """
    filterset_class = ProjectFilter
    serializer_class = SearchProjectSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Project.objects.none()
        elif user.is_admin:
            return Project.objects.all()
        elif user.is_team_manager:
            return Project.objects.filter(project_starter__in=user.team_members)
        elif user.is_developer:
            return Project.objects.filter(project_starter=user)
