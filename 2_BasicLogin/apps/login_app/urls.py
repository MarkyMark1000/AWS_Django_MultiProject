# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.login_app import views


urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', views.CustomUserCreationView.as_view(), name='register'),
    path('sent/', views.ActivationSentView.as_view(), name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.ActivateView.as_view(), name='activate'),
]
