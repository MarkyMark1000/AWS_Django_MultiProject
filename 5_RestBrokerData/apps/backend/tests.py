from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime
# Config Data
from apps.backend.apps import BackendConfig
from django.apps import apps
# Models
from apps.backend.models import PollingServerCountry
from apps.backend.models import Broker
from apps.backend.models import MonitoredAccountType
from apps.backend.models import Symbol
from apps.backend.models import MarketData

class BackEnd_NoLogin_Test(APITestCase):

    def test_apps(self):
        '''
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(BackendConfig.name, 'apps.backend')
        self.assertEqual(apps.get_app_config('backend').name,
                         'apps.backend')

    def test_pscountry_status(self):
        '''
        Test /pscountries/ for 200
        '''
        response = self.client.get('/pscountries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_pscountry(self):
        '''
        post a new PSCountry record (UK) and ensure 403 Forbidden is obtained
        and a record count of 0 now exists.
        YOU NEED TO LOGIN TO ADD A RECORD!!!
        '''
        data = {'PSCountry': 'UK'}
        response = self.client.post("/pscountries/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(PollingServerCountry.objects.count(), 0)

    def test_brokers_status(self):
        '''
        Test /brokers/ for 200
        '''
        response = self.client.get('/brokers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_broker(self):
        '''
        post a new broker record (ZZZ) and ensure 403 Forbidden is obtained
        and a record count of 0 now exists.
        YOU NEED TO LOGIN TO ADD A RECORD!!!
        '''
        data = {'name': 'ZZZ'}
        response = self.client.post("/brokers/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Broker.objects.count(), 0)

    def test_monitoredaccounttype_status(self):
        '''
        Test /monitoredaccounttype/ for 200
        '''
        response = self.client.get('/monitoredaccounttype/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_monitoredaccounttype(self):
        '''
        post a new monitoredaccounttype record, this should fail anyway
        because we would need to create a broker and pscountry and
        provide those id's, but this is here to ensure that if fails
        with 403 error because we are not logged in.
        '''
        data = {'account_type': 'PRO', 'pollingservercountry': 1, 'broker': 1}
        response = self.client.post("/monitoredaccounttype/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Broker.objects.count(), 0)

class BackEnd_LoggedIn_Test(APITestCase):

    def setUp(self):
        '''
        Within this class, create a user object and login
        '''
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.login = self.client.login(username='testuser', password='12345')

    def test_pscountry_status(self):
        '''
        Test /pscountries/ for 200
        '''
        response = self.client.get('/pscountries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _createPSCountry(self):
        '''
        This is not a test, but used by multiple tests to create a country
        It should return the id of the country
        '''
        data = {'PSCountry': 'UK'}
        response = self.client.post("/pscountries/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PollingServerCountry.objects.count(), 1)
        self.assertEqual(PollingServerCountry.objects.get().PSCountry, 'UK')

        return PollingServerCountry.objects.get().id

    def _putPSCountry(self, id):
        '''
        This is not a test, but used by multiple tests to update a country
        It should return the id of the country
        '''
        data = {'PSCountry': 'USD'}
        url = f"/pscountries/{id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PollingServerCountry.objects.count(), 1)
        self.assertEqual(PollingServerCountry.objects.get().PSCountry, 'USD')

        return PollingServerCountry.objects.get().id
    
    def _getPSCountry(self, id):
        '''
        Make sure we can get the country
        '''
        url = f"/pscountries/{id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _deletePSCountry(self, id):
        '''
        This is not a test, but used by multiple tests to delete a ps
        country
        '''
        path = "/pscountries/"+str(id)+"/"
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PollingServerCountry.objects.count(), 0)

    def test_create_and_delete_pscountry(self):
        '''
        Post a new PSCountry record, 'UK' to the server and ensure it is created.
        '''

        # Post 'UK'
        id = self._createPSCountry()

        # Update the country
        id = self._putPSCountry(id)

        # Delete Record
        self._deletePSCountry(id)

    def test_broker_status(self):
        '''
        Test /brokers/ for 200
        '''
        response = self.client.get('/brokers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _createBroker(self):
        '''
        This is not a test, but used by multiple tests to create a broker
        It should return the id of the broker
        '''
        # Post 'ZZZ'
        data = {'name': 'ZZZ'}
        response = self.client.post("/brokers/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Broker.objects.count(), 1)
        self.assertEqual(Broker.objects.get().name, 'ZZZ')

        return Broker.objects.get().id

    def _putBroker(self, id):
        '''
        This is not a test, but used by multiple tests to update a country
        It should return the id of the country
        '''
        data = {'name': 'XXX'}
        url = f"/brokers/{id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Broker.objects.count(), 1)
        self.assertEqual(Broker.objects.get().name, 'XXX')

        return Broker.objects.get().id

    def _deleteBroker(self, id):
        '''
        This is not a test, but used by multiple tests to delete a broker
        '''
        path = "/brokers/"+str(id)+"/"
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Broker.objects.count(), 0)

    def test_create_and_delete_brokers(self):
        '''
        Post a new broker record, 'ZZZ' to the server and ensure it is created.
        '''

        # Post 'UK'
        id = self._createBroker()

        # Update the broker
        id = self._putBroker(id)

        # Delete Record
        self._deleteBroker(id)

    def test_monitoredaccounttype_status(self):
        '''
        Test /monitoredaccounttype/ for 200
        '''
        response = self.client.get('/monitoredaccounttype/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _createMonitoredAccountType(self, pollingservercountry_id, broker_id):
        '''
        This is not a test, but used by multiple tests to create a monitored
        account type.   It should return it's id
        '''
        # Post a new account type
        data = {'account_type': 'PRO', 'pollingservercountry': pollingservercountry_id, 'broker': broker_id}
        response = self.client.post("/monitoredaccounttype/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MonitoredAccountType.objects.count(), 1)
        self.assertEqual(MonitoredAccountType.objects.get().account_type, 'PRO')

        return MonitoredAccountType.objects.get().id

    def _patchMonitoredAccountType(self, id):
        '''
        This is not a test, but used by multiple tests to update a country
        It should return the id of the country
        '''
        data = {'account_type': 'BASIC'}
        url = f"/monitoredaccounttype/{id}/"
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MonitoredAccountType.objects.count(), 1)
        self.assertEqual(MonitoredAccountType.objects.get().account_type, 'BASIC')

        return MonitoredAccountType.objects.get().id

    def _deleteMonitoredAccountType(self, id):
        '''
        This is not a test, but used by multiple tests to delete a MAT
        '''
        # Delete Record
        path = "/monitoredaccounttype/"+str(id)+"/"
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MonitoredAccountType.objects.count(), 0)

    def test_create_and_delete_monitoredaccounttype(self):
        '''
        Create a polling server and broker and then try to create a
        monitored account type of 'PRO' and then delete it
        '''

        psc_id = self._createPSCountry()

        broker_id = self._createBroker()

        id = self._createMonitoredAccountType(psc_id, broker_id)

        id = self._patchMonitoredAccountType(id)

        self._deleteMonitoredAccountType(id)

    def test_symbol_status(self):
        '''
        Test /symbols/ for 200
        '''
        response = self.client.get('/symbols/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _createSymbol(self):
        '''
        This is not a test, but used by multiple tests to create a Symbol
        It should return it's id
        '''
        # Post a new account type
        data = {'name': 'EURGBP'}
        response = self.client.post("/symbols/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Symbol.objects.count(), 1)
        self.assertEqual(Symbol.objects.get().name, 'EURGBP')

        return Symbol.objects.get().id

    def _putSymbol(self, id):
        '''
        This is not a test, but used by multiple tests to update a country
        It should return the id of the country
        '''
        data = {'name': 'EURUSD'}
        url = f"/symbols/{id}/"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Symbol.objects.count(), 1)
        self.assertEqual(Symbol.objects.get().name, 'EURUSD')

        return Symbol.objects.get().id

    def _deleteSymbol(self, id):
        '''
        This is not a test, but used by multiple tests to delete a sybmol
        '''
        # Delete Record
        path = "/symbols/"+str(id)+"/"
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Symbol.objects.count(), 0)

    def test_create_and_delete_symbol(self):
        '''
        Create and Delete a Symbol
        '''

        # Post 'UK'
        id = self._createSymbol()

        # Put 'UK'
        id = self._putSymbol(id)

        # Delete Record
        self._deleteSymbol(id)

    def test_marketdata_status(self):
        '''
        Test /marketdata/ for 200
        '''
        response = self.client.get('/marketdata/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_and_delete_marketdata(self):
        '''
        Create Market Data records and delete it
        '''

        # Setup all of the base records such as pollingservercountry
        # broker etc
        psc_id = self._createPSCountry()
        broker_id = self._createBroker()
        mat_id = self._createMonitoredAccountType(psc_id, broker_id)
        symbol_id = self._createSymbol()

        # Get current datetime and use for record
        dtNow = datetime.now()

        # Create the data to add to the database
        data = {'account_type':mat_id, 'name':symbol_id, 'PollDateTime':dtNow,
                'spread':0.001, 'stoplevel':0, 'freezelevel':0.0002, 'isconnected':True}

        # Add teh data via the marketdata link and test that isconnected is true
        response = self.client.post("/marketdata/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MarketData.objects.count(), 1)
        self.assertEqual(MarketData.objects.get().isconnected, True)

        # Get the id of the market data record
        idMD = MarketData.objects.get().id
        
        # Patch market data record
        path = "/marketdata/"+str(idMD)+"/"
        data = { 'spread':0.002 }
        response = self.client.patch(path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MarketData.objects.count(), 1)
        self.assertEqual(MarketData.objects.get().spread, 0.002)

        # Delete market data Record
        path = "/marketdata/"+str(idMD)+"/"
        response = self.client.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MarketData.objects.count(), 0)

class BackEnd_LoggedIn_DifferentUser_Test(APITestCase):

    def setUp(self):
        '''
        Within this class, create a user object, populate data, login
        as a different user and test permissions.
        '''
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='23456')

        #Login and populate some data
        self.login = self.client.login(username='testuser1', password='12345')

        #Create country
        data = {'PSCountry': 'UK'}
        response = self.client.post("/pscountries/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.pscountry_id = PollingServerCountry.objects.get().id

        #Create broker
        data = {'name': 'ZZZ'}
        response = self.client.post("/brokers/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.broker_id = Broker.objects.get().id

        #Logout
        self.client.logout()

        #Login to the different account
        self.login = self.client.login(username='testuser2', password='23456')

    def test_put_pscountry(self):
        '''
        Test putting the country
        '''
        url = f'/pscountries/{self.pscountry_id}'
        data = {'PSCountry': 'USA'}
        response = self.client.put(url, data, format='json')
        # This should not e allowed as we are trying to update another
        # users data
        self.assertNotEqual(PollingServerCountry.objects.get().PSCountry, 'USA')
        self.assertEqual(PollingServerCountry.objects.get().PSCountry, 'UK')

        # I could repeat this test for all of the models
