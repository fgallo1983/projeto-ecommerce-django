from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.

class Criar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('criar')

class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('atruwlkzar')

class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('login')

class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('logout')
