# Import Models
from apps.backend.models import PollingServerCountry
from apps.backend.models import Broker
from apps.backend.models import MonitoredAccountType
from apps.backend.models import Symbol
from apps.backend.models import MarketData
# Import Serializers
from apps.backend.serializers import PSCountrySerializer
from apps.backend.serializers import BrokerSerializer
from apps.backend.serializers import MonitoredAccountTypeSerializer
from apps.backend.serializers import SymbolSerializer
from apps.backend.serializers import MarketDataSerializer
# Import Permissions
from rest_framework import permissions
from apps.backend.permissions import IsOwnerOrReadOnly
# Remaining rest imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
        


'''
PSCountry classes
'''


class PSCountryList(generics.ListCreateAPIView):
    queryset = PollingServerCountry.objects.all()
    serializer_class = PSCountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PSCountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollingServerCountry.objects.all()
    serializer_class = PSCountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


'''
Broker classes
'''


class BrokerList(generics.ListCreateAPIView):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BrokerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

'''
Monitored Account Type classes
'''


class MonitoredAccountTypeList(generics.ListCreateAPIView):
    queryset = MonitoredAccountType.objects.all()
    serializer_class = MonitoredAccountTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MonitoredAccountTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MonitoredAccountType.objects.all()
    serializer_class = MonitoredAccountTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

'''
Symbol classes
'''


class SymbolList(generics.ListCreateAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SymbolDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

'''
Market Data classes
'''


class MarketDataList(generics.ListCreateAPIView):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MarketDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
