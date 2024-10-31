from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from .models import Pedido, ItemPedido
from utils import utils
from django.urls import reverse
from django.views.generic import ListView, DetailView

class Pagar(DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'
    

class SalvarPedido(View):
    template_name = 'pedido/pagar.html'
    
    def get(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')
        
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('produto:lista')
        
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho] #type:ignore
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )
        
        for variacao in bd_variacoes:
            vid = str(variacao.id) #type:ignore

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade'] #type:ignore
            preco_unt = carrinho[vid]['preco_unitario'] #type:ignore
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional'] #type:ignore
            
            error_msg_estoque = ''
            
            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque #type:ignore
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt #type:ignore
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unt_promo #type:ignore 
                
                error_msg_estoque = 'Estoque insuficiente para alguns '\
                    'produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)
        
        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )

        pedido.save()
        
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values() #type:ignore
            ]
        )
        
        del self.request.session['carrinho']
        
        contexto = {
            
        }
        
        # return render(self.request, self.template_name, contexto)
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('detalhe')

