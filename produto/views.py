from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views import View
from . import models
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib import messages

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html' 
    context_object_name = 'produtos'
    paginate_by = 10
    ordering = ['-id']
    
class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)
        
        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('remover do carrnho')

class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('carrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('finalziar')