from django.shortcuts import render
from django.views import View

class FrontEndView(View):

    def get(self, request, **kwargs):

        return render(request, 'index.html', context=None)
