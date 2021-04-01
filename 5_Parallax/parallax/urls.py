"""parallax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from parallax import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Page1View.as_view(), name='page1'),
    path('page2/', views.Page2View.as_view(), name='page2'),
    path('page3/', views.Page3View.as_view(), name='page3'),
]
