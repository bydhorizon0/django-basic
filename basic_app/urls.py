"""
URL configuration for basic_app project.

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

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

from basic_app import settings
from blog.views import post_view
from common import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", post_view.PostListView.as_view(), name="home"),
    path("signup", views.signup, name="signup"),
    path("login", views.EmailLoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ] + debug_toolbar_urls()
