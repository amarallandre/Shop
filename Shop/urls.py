from django.contrib import admin
from django.urls import path
from .views import adicionar_produto, adicionar_ao_carrinho, index, produtos_disponiveis, Finalizar_Compra, limpar_historico, Remover_produto

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('adicionar_produto/', adicionar_produto, name='adicionar_produto'),
    path('adicionar_ao_carrinho/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('produtos_disponiveis/', produtos_disponiveis, name='produtos_disponiveis'),
    path('historico/', Finalizar_Compra, name='Finalizar_Compra'),
    path('limpar_historico/', limpar_historico, name='limpar_historico'),
    path('Remover_produto/<int:produto_id>/', Remover_produto, name='Remover_produto'),

]
