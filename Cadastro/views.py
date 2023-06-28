from django.http import JsonResponse
from database.models import Cadastro, RecursosHumanos
import json


def cadastrar(request):
    if request.method == 'POST':
        decode_json = request.body.decode('utf-8')
        registro_cadastro = json.loads(decode_json)

        nome = registro_cadastro.get('nome')
        email = registro_cadastro.get('email')
        senha = registro_cadastro.get('senha')
        cargo = registro_cadastro.get('cargo')

        if not nome or not email or not senha or not cargo:
            return JsonResponse({'erro': 'Todos os campos são obrigatórios'}, status=400)

        cadastro = Cadastro(nome=nome, email=email, senha=senha, cargo=cargo)
        cadastro.save()

        return JsonResponse({'mensagem': 'Cadastro realizado com sucesso!'})

    return JsonResponse({'erro': 'Método inválido'}, status=405)


def atualizar_cadastro(request):
    if request.method == 'PUT':
        decode_json = request.body.decode('utf-8')
        dados_atualizacao = json.loads(decode_json)

        cadastro_id = dados_atualizacao.get('id')
        novo_email = dados_atualizacao.get('email')
        nova_senha = dados_atualizacao.get('senha')

        if not cadastro_id:
            return JsonResponse({'erro': 'O campo "id" é obrigatório.'}, status=400)

        try:
            cadastro = Cadastro.objects.get(id=cadastro_id)
        except Cadastro.DoesNotExist:
            return JsonResponse({'erro': 'Cadastro não encontrado.'}, status=404)

        if novo_email:
            cadastro.email = novo_email
        if nova_senha:
            cadastro.senha = nova_senha

        cadastro.save()

        return JsonResponse({'mensagem': 'Cadastro atualizado com sucesso.'})

    return JsonResponse({'erro': 'Método inválido'}, status=405)


def deletar_cadastro(request):
    if request.method == 'DELETE':
        try:
            decode_json = request.body.decode('utf-8')
            dados_exclusao = json.loads(decode_json)

            cadastro_id = dados_exclusao.get('id')

            try:
                cadastro = Cadastro.objects.get(id=cadastro_id)
            except Cadastro.DoesNotExist:
                return JsonResponse({'erro': 'Cadastro não encontrado.'}, status=404)

            try:
                recursos_humanos = RecursosHumanos.objects.get(
                    funcionario=cadastro)
                if recursos_humanos.folha_de_ponto:
                    recursos_humanos.folha_de_ponto.delete()
                recursos_humanos.delete()
            except RecursosHumanos.DoesNotExist:
                pass

            cadastro.delete()

            return JsonResponse({'mensagem': 'Cadastro excluído com sucesso.'})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    return JsonResponse({'erro': 'Método inválido'}, status=405)
