# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.stripe_elements_subscription import views

urlpatterns = [
    path('stripe_elements_sub/', views.ElementsSubView.as_view(), name="stripe_elements_sub"),
    path('stripe_elements_prices/', views.ElementsPricesView.as_view(), name="stripe_elements_prices"),
    path('stripe_elements/', views.ElementsSubPriceView.as_view(), name="stripe_elements"),
    path('stripe_elements/<price>/', views.ElementsSubPriceView.as_view(), name="stripe_elements_price"),
    path('stripe_elements_account/', views.ElementsSubAccountView.as_view(), name="stripe_elements_account"),
    path('stripe_elements_create_customer/', views.create_customer_view, name="stripe_elements_create_customer"),
    path('stripe_elements_create_subscription/', views.create_subscription_view, name="stripe_elements_create_subscription"),
    path('stripe_elements_list_subscriptions/', views.list_subscriptions_view, name="stripe_elements_list_subscriptions"),
    # Beware these two - there are 2 different cancel operations.
    path('stripe_elements_cancel_subscription/', views.cancel_subscription_view, name="stripe_elements_cancel_subscription"),
    path('stripe_elements_cancel_subscription/<subscription_id>/', views.ElementsCancelView.as_view(), name="stripe_elements_cancel_subscription_id"),
    path('stripe_elements_sub_webhook/', views.my_webhook_view, name="stripe_elements_sub_webhook"),
]
