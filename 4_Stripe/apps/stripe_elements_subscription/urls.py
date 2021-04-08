# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.stripe_elements_subscription import views

urlpatterns = [
    path('stripe_elements_sub/', views.ElementsSubView.as_view(), name="stripe_elements_sub"),
]