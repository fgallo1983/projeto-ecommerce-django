from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.

class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('pagar')

class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Salvar pedido')

class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('detalhe')

