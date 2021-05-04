from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from brokerdata.settings import BASE_DIR
'''
Front End Class

'''

class FrontEnd(APIView):
    """
    A view that returns a templated HTML representation of the front end.
    It should be the only page that returns an html page
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):

        DJANGO_DEBUG = os.getenv('DJANGO_DEBUG', 'True')
        API_ENVIRONMENT = os.getenv('API_ENVIRONMENT', 'test')
        
        return Response({'DJANGO_DEBUG': DJANGO_DEBUG,
                         'API_ENVIRONMENT': API_ENVIRONMENT,
                         'BASE_DIR': BASE_DIR})
