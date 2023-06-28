from django.http import JsonResponse
from database.models import Cadastro, RecursosHumanos
import json


def cadastrar_funcionario(request):
    if request.method == 'POST':
        try:
            decode_json = request.POST.get('json_data')
            if not decode_json:
                return JsonResponse({'erro': 'Dados do funcionário não fornecidos.'}, status=400)

            registro_funcionario = json.loads(decode_json)

            funcionario_id = registro_funcionario.get('funcionario_id')
            salario = registro_funcionario.get('salario')
            carga_horaria = registro_funcionario.get('carga_horaria')
            setor = registro_funcionario.get('setor')

            folha_de_ponto = request.FILES.get('folha_de_ponto')
            if not folha_de_ponto:
                return JsonResponse({'erro': 'Folha de ponto não fornecida.'}, status=400)

            if not funcionario_id or not salario or not carga_horaria or not setor:
                return JsonResponse({'erro': 'Todos os campos são obrigatórios.'}, status=400)

            try:
                funcionario = Cadastro.objects.get(id=funcionario_id)
            except Cadastro.DoesNotExist:
                return JsonResponse({'erro': 'Funcionário não encontrado.'}, status=404)

            recursos_humanos = RecursosHumanos(
                funcionario=funcionario, salario=salario, carga_horaria=carga_horaria, setor=setor,
                folha_de_ponto=folha_de_ponto
            )
            recursos_humanos.save()

            folha_de_ponto_url = recursos_humanos.folha_de_ponto.url

            response_data = {
                'status': 'Cadastro de funcionário realizado com sucesso',
                'registro': {
                    'nome': funcionario.nome,
                    'email': funcionario.email,
                    'cargo': funcionario.cargo,
                    'salario': recursos_humanos.salario,
                    'carga_horaria': recursos_humanos.carga_horaria,
                    'setor': recursos_humanos.setor,
                    'folha_de_ponto_url': folha_de_ponto_url
                }
            }

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    return JsonResponse({'erro': 'Método inválido'}, status=405)


def buscar_funcionarios(request):
    if request.method == 'GET':
        try:

            funcionarios = RecursosHumanos.objects.all()
            dados_funcionarios = []

            for recurso in funcionarios:
                dados_funcionario = {
                    'id': recurso.funcionario.id,
                    'nome': recurso.funcionario.nome,
                    'cargo': recurso.funcionario.cargo,
                    'salario': recurso.salario,
                    'carga_horaria': recurso.carga_horaria,
                    'setor': recurso.setor,
                    'folha_de_ponto_url': recurso.folha_de_ponto.url if recurso.folha_de_ponto else None
                }
                dados_funcionarios.append(dados_funcionario)

            return JsonResponse({'funcionarios': dados_funcionarios})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    return JsonResponse({'erro': 'Método inválido'}, status=405)
