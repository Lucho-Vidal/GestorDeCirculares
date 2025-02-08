"""
URL configuration for GestorDeCirculares project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from formulario import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.signIn, name='signin'),
    path('signup/', views.signUp, name='signup'),
    path('logout/', views.signOut, name='logout'),
    path('circulares/', views.circulares, name='circulares'),
    path('circularesCompleted/', views.circularesCompleted, name='circularesCompleted'),
    path('circularDetalle/<int:id>/', views.circularDetalle, name='circularDetalle'),
    path('circularDetalle/<int:id>/complete', views.completeCircular, name='completeCircular'),
    path('circularDetalle/<int:id>/delete', views.deleteCircular, name='deleteCircular'),
    path('createCircular/', views.createCircular, name='createCircular'),
]
