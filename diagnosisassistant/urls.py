"""
URL configuration for diagnosisassistant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import CustomTokenObtainPairView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('managementdataset.urls')),
    path('', include('managementdoctor.urls')),
    path('', include('managementhospital.urls')),
    path('api/v1/', include('managementpacient.urls')),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Custom login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('logout/', LogoutView.as_view(), name ='logout'),  # Logout
    path('', include('similaritysearch.urls'))
]
