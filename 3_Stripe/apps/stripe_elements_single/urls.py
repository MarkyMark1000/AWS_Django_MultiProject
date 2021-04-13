# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.stripe_elements_single import views

urlpatterns = [
    path('stripe_elements_checkout/', views.CheckoutView.as_view(), name="stripe_elements_checkout"),
    path('stripe_elements_checkout2/', views.Checkout2View.as_view(), name="stripe_elements_checkout2"),
    path('stripe_elements_create_payment_intent/', views.create_payment_intent_view, name="stripe_elements_create_payment_intent"),
    path('stripe_elements_webhook/', views.my_webhook_view, name="stripe_elements_webhook"),
]