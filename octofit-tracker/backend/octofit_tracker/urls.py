"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import os
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import UserViewSet, TeamViewSet, ActivityViewSet, LeaderboardViewSet, WorkoutViewSet, api_root



# Patch the router to use the codespace URL in browsable API root links
class CodespaceRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        api_root_view = super().get_api_root_view(api_urls)
        codespace_name = os.environ.get('CODESPACE_NAME')
        base_url = None
        if codespace_name:
            base_url = f"https://{codespace_name}-8000.app.github.dev"

        def view(request, *args, **kwargs):
            # Patch request.build_absolute_uri to use codespace URL if available
            if base_url:
                orig_build_absolute_uri = request.build_absolute_uri
                def custom_build_absolute_uri(location=None):
                    uri = orig_build_absolute_uri(location)
                    # Replace the scheme+host with codespace URL
                    if uri.startswith('http://') or uri.startswith('https://'):
                        # Find the first single slash after scheme
                        idx = uri.find('/', uri.find('//') + 2)
                        if idx != -1:
                            uri = base_url + uri[idx:]
                        else:
                            uri = base_url
                    return uri
                request.build_absolute_uri = custom_build_absolute_uri
            return api_root_view(request, *args, **kwargs)
        return view

router = CodespaceRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', api_root, name='api-root'),
]
