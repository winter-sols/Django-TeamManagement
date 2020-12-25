from django.urls import  include, path
from .user.views import UserAdminViewSet, TeamListViewSet, ProfileListAdminView, ProfilesAdminViewSet, AccountListByProfileIdView, AccountsAdminViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserAdminViewSet)
router.register('teams', TeamListViewSet)
router.register('profiles', ProfilesAdminViewSet)
router.register('accounts', AccountsAdminViewSet)

urlpatterns = router.urls + [
    path('users/<int:pk>/profiles', ProfileListAdminView.as_view(), name='profiles-by-user_id'),
    path('profiles/<int:pk>/accounts', AccountListByProfileIdView.as_view(), name='profiles-by-user_id'),
]
