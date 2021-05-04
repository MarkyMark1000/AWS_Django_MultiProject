from django.db import models


class PollingServerCountry(models.Model):
    PSCountry = models.CharField(max_length=40, blank=True, null=False)
    owner = models.ForeignKey('auth.User', related_name='PollingServerCountries',
                              on_delete=models.CASCADE)

    class Meta:
        ordering = ['PSCountry']


class Broker(models.Model):
    name = models.CharField(max_length=40, blank=True, null=False)
    psc = models.ManyToManyField(PollingServerCountry,through='MonitoredAccountType')
    owner = models.ForeignKey('auth.User', related_name='Brokers',
                              on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']


class MonitoredAccountType(models.Model):
    account_type = models.CharField(max_length=40, blank=True, null=False)
    pollingservercountry = models.ForeignKey(PollingServerCountry, blank=True, null=False, on_delete=models.CASCADE, related_name="MonitoredAccountTypes_psc")
    broker = models.ForeignKey(Broker, blank=True, null=False, on_delete=models.CASCADE, related_name="Broker")
    owner = models.ForeignKey('auth.User', related_name='MonitoredAccountTypes',
                              on_delete=models.CASCADE)


class Symbol(models.Model):
    name = models.CharField(max_length=40, blank=True, null=False)
    owner = models.ForeignKey('auth.User', related_name='Symbols',
                              on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']


class MarketData(models.Model):
    account_type = models.ForeignKey(MonitoredAccountType, blank=True, null=False, on_delete=models.CASCADE, related_name="MonitoredAccountType")
    name = models.ForeignKey(Symbol, blank=True, null=False, on_delete=models.CASCADE, related_name="Symbol")
    PollDateTime = models.DateTimeField(blank=True, null=False)
    spread = models.FloatField(blank=True, null=False)
    stoplevel = models.FloatField(blank=True, null=False)
    freezelevel = models.FloatField(blank=True, null=False)
    isconnected = models.BooleanField(blank=True, null=False)
    owner = models.ForeignKey('auth.User', related_name='MarketData',
                              on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['account_type','name','PollDateTime'], name='AcctSymbDateTime_Idx')
        ]