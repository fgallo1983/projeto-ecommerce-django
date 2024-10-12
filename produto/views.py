from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models
from django.views.generic.detail import DetailView
from django.http import HttpResponse

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html' 
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']
    
class DetalheProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('detalhes prouto')

class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('adiiconar ao carrinho')

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('remover do carrnho')

class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('carrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('finalziar')