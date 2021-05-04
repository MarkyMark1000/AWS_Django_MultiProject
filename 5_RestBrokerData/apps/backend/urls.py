from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from apps.backend import views

urlpatterns = [
    path('pscountries/', views.PSCountryList.as_view(), name="pscountries"),
    path('pscountries/<int:pk>/', views.PSCountryDetail.as_view()),
    path('brokers/', views.BrokerList.as_view(), name="brokers"),
    path('brokers/<int:pk>/', views.BrokerDetail.as_view()),
    path('monitoredaccounttype/', views.MonitoredAccountTypeList.as_view(), name="monitoredaccounttype"),
    path('monitoredaccounttype/<int:pk>/', views.MonitoredAccountTypeDetail.as_view()),
    path('symbols/', views.SymbolList.as_view(), name="symbols"),
    path('symbols/<int:pk>/', views.SymbolDetail.as_view()),
    path('marketdata/', views.MarketDataList.as_view(), name="marketdata"),
    path('marketdata/<int:pk>/', views.MarketDataDetail.as_view()),
]

# This was added
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]