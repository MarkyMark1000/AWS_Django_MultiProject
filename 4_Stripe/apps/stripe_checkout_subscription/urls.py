# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.stripe_checkout_subscription import views


urlpatterns = [
    path('stripe_basic_sub/', views.BasicSubscriptionView.as_view(), name="stripe_basic_sub"),
    path('stripe_sub_setup/', views.stripe_sub_setup, name="stripe_sub_setup"),
    path('stripe_sub_create_checkout_session/', views.create_checkout_session, name="stripe_sub_create_checkout_session"),
    path('stripe_sub_success/', views.SubSuccessView.as_view(), name="stripe_sub_success"),
    path('stripe_sub_success/<session_id>/', views.SubSuccessView.as_view(), name="stripe_sub_success_id"),
    path('stripe_sub_cancel/', views.SubCancelView.as_view(), name="stripe_sub_cancel"),
    path('stripe_sub_checkout_session/', views.checkout_session, name="stripe_checkout_session"),
    path('stripe_sub_checkout_session/<session_id>/', views.checkout_session, name="stripe_checkout_session_id"),
    path('stripe_sub_customer_portal/', views.customer_portal, name="stripe_sub_customer_portal"),
    path('stripe_sub_finished_billing/', views.SubFinishedBillingView.as_view(), name="stripe_sub_finished_billing"),
    path('privacy/', views.PrivacyView.as_view(), name="stripe_sub_privacy"),
    path('terms/', views.TermsView.as_view(), name="stripe_sub_terms"),
    path('stripe_sub_webhook/', views.my_webhook_view, name="stripe_su_webhook"),
]
