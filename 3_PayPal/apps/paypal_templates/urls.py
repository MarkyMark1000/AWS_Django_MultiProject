# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.paypal_templates import views


urlpatterns = [
    path('paypal_sandbox/', views.SandboxView.as_view(), name="paypal_sandbox"),
    path('paypal_verybasic/', views.VeryBasicView.as_view(), name="paypal_very_basic"),
    path('paypal_success/', views.SuccessView.as_view(), name="paypal_success"),
]
