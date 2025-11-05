from django.db import models
from produtos.models import Produto
from ingredientes.models import Ingrediente
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MinValueValidator  # Importação corrigida

class Compra(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name='compras')
    quantidade_comprada = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_compra = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Atualiza o estoque do ingrediente
        ingrediente = self.ingrediente
        ingrediente.quantidade_estoque += self.quantidade_comprada
        ingrediente.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra de {self.quantidade_comprada} {self.ingrediente.unidade_medida} de {self.ingrediente.nome}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

class GastoFixo(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data = models.DateTimeField(default=timezone.now)
    dia_pagamento = models.PositiveSmallIntegerField(default=1, help_text="Dia do mês para pagamento (1-31)")

    def __str__(self):
        return f"{self.descricao} - R${self.valor} (Dia {self.dia_pagamento})"

    class Meta:
        verbose_name = "Gasto Fixo"
        verbose_name_plural = "Gastos Fixos"

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='vendas')
    quantidade_vendida = models.PositiveIntegerField(default=1)
    data_venda = models.DateTimeField(default=timezone.now)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        # Calcular valor total e atualizar estoque
        self.valor_total = self.quantidade_vendida * self.produto.preco_venda
        produto = self.produto
        if produto.quantidade_estoque >= self.quantidade_vendida:
            produto.quantidade_estoque -= self.quantidade_vendida
            produto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda de {self.quantidade_vendida} {self.produto.nome}"

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"