from django.urls import  include, path
from .user.views import UserAdminViewSet, TeamListViewSet, ProfileListAdminView, ProfilesAdminViewSet, AccountListByProfileIdView, AccountsAdminViewSet, TeamUserListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserAdminViewSet)
router.register('teams', TeamListViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)

urlpatterns = router.urls + [
    path('users/<int:pk>/profiles/', ProfileListAdminView.as_view(), name='user_profiles'),
    path('profiles/<int:pk>/accounts/', AccountListByProfileIdView.as_view(), name='profile_accounts'),
    path('teams/<int:pk>/users/', TeamUserListView.as_view(), name='users_by_team_id')
]
