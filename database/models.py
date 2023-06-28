from django.db import models

# Create your models here.


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    quantidade_estoque = models.PositiveIntegerField()
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    setor = models.CharField(max_length=50)
    corredor = models.PositiveIntegerField()
    prateleira = models.PositiveIntegerField()
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.produto} ({self.setor})'


class Compra(models.Model):
    nome_produto = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)
    nome_fornecedor = models.CharField(max_length=50)

    def __str__(self):
        return f"Compra: {self.nome_produto} ({self.data_compra.strftime('%Y-%m-%d %H:%M:%S')})"


class Venda(models.Model):
    produtos = models.JSONField()
    preco_total = models.DecimalField(
        max_digits=10, decimal_places=2)
    data_venda = models.DateTimeField(auto_now_add=True)
    metodo_pagamento = models.CharField(max_length=50)
    parcelas = models.PositiveIntegerField()
    id_caixa = models.PositiveIntegerField()

    def __str__(self):
        return f"Venda: ({self.data_venda.strftime('%Y-%m-%d %H:%M:%S')})"


class Cadastro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Login(models.Model):
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cadastro.email}: ({self.data_hora.strftime('%Y-%m-%d %H:%M:%S')})"


class RecursosHumanos(models.Model):
    funcionario = models.OneToOneField(Cadastro, on_delete=models.CASCADE)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    carga_horaria = models.IntegerField()
    folha_de_ponto = models.FileField(upload_to='folhas_ponto/')
    setor = models.CharField(max_length=50)

    def __str__(self):
        return self.funcionario.nome
