"""FM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashing/', include('dashing.urls')),
    path('', include('pages.urls')),
    path('contact/', include('contact.urls')),
    #pypath('notification/', include('notification.urls')),

    # User management
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),  # add django's build-in auth module
    #path('accounts/', include('allauth.urls')),   # 3rd party auth module

]