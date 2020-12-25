from django.urls import  include, path


urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('admin/', include('api.admin.urls')),
    path('team-manager/', include('api.team_manager.urls'))
]