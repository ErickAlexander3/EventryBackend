"""eventry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
#from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from authapp.views import FacebookLogin, GoogleLogin, privacy_policy#, UserViewSet
from events.views import EventViewSet

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'events', EventViewSet)
#router.register(r'users', UserViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('privacy_policy/', privacy_policy, name='privacy_policy'),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
	#path('events/', include('events.urls')),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
