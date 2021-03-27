# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.stripe_checkout_single import views


urlpatterns = [
    path('stripe_test_data/', views.TestDataView.as_view(), name="stripe_test_data"),
    path('stripe_success/', views.SuccessView.as_view(), name="stripe_success"),
    path('stripe_cancel/', views.CancelView.as_view(), name="stripe_cancel"),
    path('stripe_basic/', views.BasicView.as_view(), name="stripe_basic"),
    path('stripe_create_checkout_session/', views.checkout_session_view,
         name="stripe_create_checkout_session"),
    path('webhook/', views.my_webhook_view, name="webhook"),
]
