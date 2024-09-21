"""
URL configuration for weGrow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viegit
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path,include
from rest_framework.routers import DefaultRouter

from .views import *
router = DefaultRouter()
#
# router.register(r'check-is-admin', CheckIsAdminViewSet, basename="检测用户是否是管理员")  # 检测用户是否是管理员
# router.register(r'user', UserListViewSet, basename="用户管理")

urlpatterns = [
    re_path('^admin/', CheckIsAdminViewSet),
]
