"""
URL configuration for blog_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from users import router as users_api_router
from blog import router as blog_api_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)


auth_api_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

if settings.DEBUG:
    auth_api_urls.append(path('verify/', include('rest_framework.urls'), ))


api_url_pattern = [
    path('accounts/', include(users_api_router.urlpatterns)),
    path('auth/', include(auth_api_urls)),
    # path('blog/', include('blog.router')),
    path('blog/', include(blog_api_router.urlpatterns)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_pattern)),
]
