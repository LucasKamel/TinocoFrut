from django.http import JsonResponse
from database.models import Compra, Produto, Venda
import json
from django.utils import timezone


def comprar(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        if not data.get('nome_produto') or not data.get('preco') or \
                not data.get('quantidade') or not data.get('nome_fornecedor'):

            return JsonResponse({"status": "Erro", "mensagem": "Todos os campos são obrigatórios."})

        nome_produto = data.get('nome_produto')
        preco = float(data.get('preco'))
        quantidade = int(data.get('quantidade'))
        nome_fornecedor = data.get('nome_fornecedor')
        preco_total = preco * quantidade
        data_compra = timezone.now()

        compra = Compra(nome_produto=nome_produto, preco=preco, quantidade=quantidade,
                        preco_total=preco_total, data_compra=data_compra, nome_fornecedor=nome_fornecedor)
        compra.save()

        produto = Produto.objects.get(nome=nome_produto)
        produto.quantidade_estoque += quantidade
        produto.save()

        response_data = {
            "status": "Registro de compra realizado com sucesso",
            "registro": {
                "nome_produto": compra.nome_produto,
                "preco": str(compra.preco),
                "quantidade": compra.quantidade,
                "preco_total": str(compra.preco_total),
                "data_compra": compra.data_compra.strftime("%Y-%m-%d %H:%M:%S"),
                "nome_fornecedor": compra.nome_fornecedor
            }
        }

        return JsonResponse(response_data)

    return JsonResponse({'Mensagem': 'Método inválido.'}, status=405)


def vender(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        if not data.get('produtos') or not data.get('metodo_pagamento') \
                or not data.get('parcelas') or not data.get('id_caixa'):
            return JsonResponse({"status": "Erro", "mensagem": "Todos os campos são obrigatórios."})

        produtos = data.get('produtos')
        metodo_pagamento = data.get('metodo_pagamento')
        parcelas = int(data.get('parcelas'))
        id_caixa = int(data.get('id_caixa'))

        preco_total = 0

        for produto in produtos:
            if not produto.get('preco') or not produto.get('quantidade'):
                return JsonResponse({"status": "Erro", "mensagem": "Todos os campos de produto são obrigatórios."})

            preco = float(produto.get('preco'))
            quantidade = int(produto.get('quantidade'))
            preco_total += preco * quantidade

        venda = Venda(produtos=produtos,
                      preco_total=preco_total,
                      data_venda=timezone.now(),
                      metodo_pagamento=metodo_pagamento,
                      parcelas=parcelas,
                      id_caixa=id_caixa)
        venda.save()

        for produto in produtos:
            nome_produto = produto.get('nome_produto')
            quantidade_vendida = produto.get('quantidade')

            produto_obj = Produto.objects.get(nome=nome_produto)

            produto_obj.quantidade_estoque -= quantidade_vendida
            produto_obj.save()

        response_data = {
            "status": "Registro de venda realizado com sucesso",
            "registro": {
                "produtos": venda.produtos,
                "preco_total": venda.preco_total,
                "data_venda": venda.data_venda.strftime("%Y-%m-%d %H:%M:%S"),
                "metodo_pagamento": venda.metodo_pagamento,
                "parcelas": venda.parcelas,
                "id_caixa": venda.id_caixa
            }
        }

        return JsonResponse(response_data)

    return JsonResponse({'Mensagem': 'Método inválido.'})


def relatorio_compras(request):

    if request.method == 'GET':
        compras = Compra.objects.all()
        compras_data = []

        for compra in compras:
            compra_data = {
                "id": compra.id,
                "nome_produto": compra.nome_produto,
                "preco": str(compra.preco),
                "quantidade": compra.quantidade,
                "preco_total": str(compra.preco_total),
                "data_compra": compra.data_compra.strftime("%Y-%m-%d %H:%M:%S"),
                "nome_fornecedor": compra.nome_fornecedor
            }
            compras_data.append(compra_data)

        response_data = {
            "status": "Consulta de compras realizada com sucesso",
            "compras": compras_data
        }

        return JsonResponse(response_data)

    return JsonResponse({'Mensagem': 'Método inválido.'})


def relatorio_vendas(request):

    if request.method == 'GET':
        vendas = Venda.objects.all()
        vendas_data = []

        for venda in vendas:
            venda_data = {
                "id": venda.id,
                "produtos": venda.produtos,
                "preco_total": str(venda.preco_total),
                "data_venda": venda.data_venda.strftime("%Y-%m-%d %H:%M:%S"),
                "metodo_pagamento": venda.metodo_pagamento,
                "parcelas": venda.parcelas,
                "id_caixa": venda.id_caixa
            }
            vendas_data.append(venda_data)

        response_data = {
            "status": "Consulta de vendas realizada com sucesso",
            "vendas": vendas_data
        }

        return JsonResponse(response_data)

    return JsonResponse({'Mensagem': 'Método inválido.'})
