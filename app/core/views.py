from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'