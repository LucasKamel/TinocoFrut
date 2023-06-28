from django.http import JsonResponse
from database.models import Produto
import json


def cadastrar_produto(request):

    if request.method == 'POST':
        decode_json = request.body.decode('utf-8')
        registro_produto = json.loads(decode_json)

        nome = registro_produto.get('nome')
        quantidade_estoque = registro_produto.get('quantidade_estoque')
        descricao = registro_produto.get('descricao')
        preco = registro_produto.get('preco')
        categoria = registro_produto.get('categoria')
        tipo = registro_produto.get('tipo')

        if not nome or not quantidade_estoque or not descricao or not preco or not categoria or not tipo:
            return JsonResponse({"status": "Erro", "mensagem": "Todos os campos são obrigatórios."})

        try:
            quantidade_estoque = int(quantidade_estoque)
            preco = float(preco)
            if quantidade_estoque <= 0 or preco <= 0:
                return JsonResponse({"status": "Erro", "mensagem": "A quantidade em estoque e o preço devem ser números positivos."})
        except ValueError:
            return JsonResponse({"status": "Erro", "mensagem": "A quantidade em estoque e o preço devem ser números válidos."})

        produto = Produto(
            nome=nome,
            quantidade_estoque=quantidade_estoque,
            descricao=descricao,
            preco=preco,
            categoria=categoria,
            tipo=tipo
        )
        produto.save()

        return JsonResponse({
            "status": "Cadastro de produto realizado com sucesso",
            "registro": {
                "nome": nome,
                "quantidade_estoque": quantidade_estoque,
                "descricao": descricao,
                "preco": preco,
                "categoria": categoria,
                "tipo": tipo
            }
        })

    return JsonResponse({'mensagem': 'Método inválido.'}, status=405)
