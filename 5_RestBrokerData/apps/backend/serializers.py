from rest_framework import serializers
# Import Models
from apps.backend.models import PollingServerCountry
from apps.backend.models import Broker
from apps.backend.models import MonitoredAccountType
from apps.backend.models import Symbol
from apps.backend.models import MarketData

class PSCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = PollingServerCountry
        fields = ['id', 'PSCountry']

class BrokerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Broker
        fields = ['id', 'name']

class MonitoredAccountTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonitoredAccountType
        fields = ['id', 'account_type', 'pollingservercountry', 'broker']

class SymbolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symbol
        fields = ['id', 'name']

class MarketDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketData
        fields = ['id', 'account_type', 'name', 'PollDateTime', 'spread','stoplevel','freezelevel','isconnected']
