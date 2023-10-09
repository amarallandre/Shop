from django.contrib import admin
from django.urls import path
from Shop.views import adicionar_produto, Remover_produto, index, produtos_disponiveis, Finalizar_Compra, limpar_historico

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('adicionar_produto/', adicionar_produto, name='adicionar_produto'),
    path('produtos_disponiveis/', produtos_disponiveis, name='produtos_disponiveis'),
    path('historico/', Finalizar_Compra, name='Finalizar_Compra'),
    path('limpar_historico/', limpar_historico, name='limpar_historico'),
    path('Remover_produto/<int:produto_id>/', Remover_produto, name='Remover_produto'),

]
