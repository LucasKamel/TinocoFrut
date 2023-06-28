from django.http import JsonResponse
from database.models import Estoque, Produto
import json
from django.core import serializers


def adicionar_estoque(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            estoque_data = data.get('estoque')

            if not produto_id or not estoque_data:
                return JsonResponse({'Erro': 'Todos os campos são obrigatórios.'}, status=400)

            produto = Produto.objects.get(id=produto_id)

            estoque = Estoque.objects.create(
                setor=estoque_data.get('setor'),
                corredor=estoque_data.get('corredor'),
                prateleira=estoque_data.get('prateleira'),
                produto=produto
            )

            response_data = {
                "status": "Produto adicionado ao estoque",
                "registro": {
                    "setor": estoque.setor,
                    "corredor": estoque.corredor,
                    "prateleira": estoque.prateleira,
                    "produto": {
                        "nome": produto.nome,
                        "quantidade_estoque": produto.quantidade_estoque,
                        "descricao": produto.descricao,
                        "preco": str(produto.preco),
                        "categoria": produto.categoria,
                        "tipo": produto.tipo
                    }
                }
            }

            return JsonResponse(response_data, status=201)
        except Produto.DoesNotExist:
            return JsonResponse({'Erro': 'Produto não encontrado.'}, status=404)

    return JsonResponse({'mensagem': 'Método inválido.'}, status=405)


def buscar_produto(request, id):
    if request.method == 'GET':
        try:
            produto = Produto.objects.get(pk=id)

            estoque = Estoque.objects.filter(produto=produto).first()

            resposta_json = {
                "produto": {
                    "id": produto.pk,
                    "nome": produto.nome,
                    "quantidade_estoque": produto.quantidade_estoque,
                    "descricao": produto.descricao,
                    "preco": str(produto.preco),
                    "categoria": produto.categoria,
                    "tipo": produto.tipo
                },
                "estoque": {
                    "setor": estoque.setor,
                    "corredor": estoque.corredor,
                    "prateleira": estoque.prateleira
                }
            }

            return JsonResponse(resposta_json, safe=False)
        except Produto.DoesNotExist:
            return JsonResponse({'Erro': 'Produto não encontrado.'}, status=404)

    return JsonResponse({'mensagem': 'Método inválido.'}, status=405)


def listar_produtos(request):
    if request.method == 'GET':
        query_set = Produto.objects.all()
        query_serializer = serializers.serialize('json', query_set)
        produtos_json = json.loads(query_serializer)

        resposta_json = []

        for produto_json in produtos_json:
            produto = produto_json['fields']
            produto_id = produto_json['pk']

            estoque = Estoque.objects.filter(produto_id=produto_id).first()

            if estoque:
                produto['estoque'] = {
                    "setor": estoque.setor,
                    "corredor": estoque.corredor,
                    "prateleira": estoque.prateleira
                }

            resposta_json.append(produto)

        return JsonResponse(resposta_json, safe=False)

    return JsonResponse({'mensagem': 'Método inválido.'}, status=405)
