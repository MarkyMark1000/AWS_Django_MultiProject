from django.shortcuts import render
from django.views import View
from django.core.exceptions import SuspiciousOperation, ValidationError


class FrontEndView(View):

    def get(self, request, **kwargs):
        return render(request, 'index.html')
