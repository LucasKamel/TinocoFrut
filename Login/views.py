from django.http import JsonResponse
from database.models import Cadastro, Login
import json
import re


def realizar_login(request):
    if request.method == 'POST':
        decode_json = request.body.decode('utf-8')
        dados_login = json.loads(decode_json)

        email = dados_login.get('email')
        senha = dados_login.get('senha')

        email_valido = re.match(
            r'^[\w\.-]+@[\w\.-]+\.\w+$', email) if email else None

        if email_valido:
            try:
                usuario = Cadastro.objects.get(email=email)

                if usuario.senha == senha:

                    novo_login = Login(cadastro=usuario)
                    novo_login.save()

                    return JsonResponse({'mensagem': 'Login realizado com sucesso!'})
                else:
                    return JsonResponse({'erro': 'Senha incorreta.'}, status=401)
            except Cadastro.DoesNotExist:
                return JsonResponse({'erro': 'Usuário não encontrado.'}, status=404)
        else:
            return JsonResponse({'erro': 'Email inválido.'}, status=400)

    return JsonResponse({'erro': 'Método inválido'}, status=405)
