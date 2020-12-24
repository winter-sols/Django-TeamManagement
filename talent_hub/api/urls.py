from django.urls import  include, path


urlpatterns = [
    path('admin/', include('api.admin.urls')),
    path('team-manager/', include('api.team_manager.urls'))
]
