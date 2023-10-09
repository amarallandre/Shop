import json
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models.produto import Produto
from .forms import ProdutoForm
from django.views.decorators.csrf import csrf_exempt
from .models.compra import Compra
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def index(request):
    produtos = Produto.objects.all()
    return render(request, 'index.html', {'produtos': produtos})

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProdutoForm()
    return render(request, 'adicionar_produto.html', {'form': form})

def Remover_produto(request, produto_id):
    if request.method == 'POST':

        logger.info(f"Solicitação para remover produto ID {produto_id}")


        produto = get_object_or_404(Produto, id=produto_id)
        produto.delete()

        return JsonResponse({'mensagem': 'Produto removido com sucesso'})
    else:
        return JsonResponse({'mensagem': 'Método não permitido'}, status=405) 

def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            produto_id = data.get('produto_id')
            quantidade = data.get('quantidade', 1)

            if produto_id and quantidade is not None:
                produto = get_object_or_404(Produto, pk=produto_id)

                carrinho = {
                    'produto': produto.nome,
                    'quantidade': int(quantidade),
                    'preco_unitario': float(produto.preco),
                }
                
                

                return JsonResponse({'status': 'success', 'carrinho': carrinho})
            else:
                return JsonResponse({'status': 'error', 'message': 'Parâmetros inválidos'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': f'Erro ao decodificar JSON: {str(e)}'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método inválido'})
    
    
def produtos_disponiveis(request):
    produtos = Produto.objects.all()
    data = [{'id': produto.id, 'nome': produto.nome, 'preco': str(produto.preco)} for produto in produtos]
    return JsonResponse(data, safe=False)



@csrf_exempt
def Finalizar_Compra(request):
    try:
        if request.method == 'POST':
            with transaction.atomic():
                data = json.loads(request.body.decode('utf-8'))
                itens_do_carrinho = data.get('itens_do_carrinho', [])
                nova_compra = Compra.objects.create()

                total_preco = 0 

                for item in itens_do_carrinho:
                    produto_id = item.get('produto_id')
                    quantidade = item.get('quantidade')
                    preco_unitario = item.get('preco_unitario')

                    produto = Produto.objects.get(pk=produto_id)

                    subtotal = quantidade * preco_unitario
                    total_preco += subtotal

                    nova_compra.produtos.add(produto, through_defaults={
                        'quantidade': quantidade,
                        'subtotal': subtotal,
                        'nome_produto': produto.nome,
                    })
                
                return JsonResponse({'mensagem': 'Compra finalizada com sucesso.', 'total_preco': total_preco})

        elif request.method == 'GET':
            historico_compras = Compra.objects.all()
            data = []

            for compra in historico_compras:
                produtos_info = []
                total_compra = 0

                for produto_rel in compra.produtos.through.objects.filter(compra=compra):
                    produto = produto_rel.produto
                    subtotal = produto_rel.subtotal
                    total_compra += subtotal
                    produtos_info.append({
                        'nome': produto.nome,
                        'preco_unitario': produto_rel.preco_unitario,
                        'quantidade': produto_rel.quantidade,
                        'subtotal': subtotal
                    })

                data.append({'id': compra.id, 'produtos': produtos_info, 'total_compra': total_compra})

            return render(request, 'historico.html', {'mensagem': 'Compra finalizada com sucesso.', 'total_preco': total_preco})

    except json.JSONDecodeError as e:
        mensagem = f'Erro ao decodificar JSON: {str(e)}'
    except Produto.DoesNotExist:
        mensagem = 'Produto não encontrado.'
    except Exception as e:
        mensagem = f'Erro ao finalizar compra: {str(e)}'

        return render(request, 'historico.html', {'historico_compras': data})

    else:
        return JsonResponse({'mensagem': 'Método não permitido.'}, status=405)
    
def limpar_historico(request):
    Compra.objects.all().delete()
    return redirect('index')