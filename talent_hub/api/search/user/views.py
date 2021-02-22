from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
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


class SearchUserView(ListAPIView):
    """
    search User by username, first_name, last_name field start with given keyword
    """
    queryset = User.objects.all()
    serializer_class = SearchUserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']


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
    queryset = Project.objects.all()
    serializer_class = SearchProjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
