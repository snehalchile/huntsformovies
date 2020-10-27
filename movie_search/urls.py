"""movie_search URL Configuration

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
from django.urls import path
import users.views as UV
import search_engine.views as SV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/login', UV.login, name='login-user'),
    path('api/user/register', UV.register, name='register-user'),
    path('api/user/logout', UV.logout, name='logout-user'),  
    path('api/admin/register', UV.register, name='register-admin'),
    path('api/admin/add-movie-details', UV.movies_details, name='add_movie_details'),
    path('api/admin/delete-movie', UV.movies_details, name='delete_movie'),
    path('api/admin/update-movie', UV.movies_details, name='update_movie'),
    path('api/search-movies', SV.search_movies, name='search_movies'),
]
