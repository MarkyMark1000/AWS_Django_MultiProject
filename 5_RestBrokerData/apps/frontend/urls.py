from django.urls import path, include
from apps.frontend import views

urlpatterns = [
    path('', views.FrontEnd.as_view(), name="frontend"),
]
