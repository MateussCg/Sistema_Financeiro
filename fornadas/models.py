# fornada/models.py
from django.db import models, transaction
from receitas.models import Receita
from produtos.models import Produto
from ingredientes.models import Ingrediente
from decimal import Decimal

class Fornada(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='fornadas')
    data_producao = models.DateTimeField(auto_now_add=True)
    quantidade_produzida = models.PositiveIntegerField(default=1, help_text="Número de execuções da receita")
    produto_gerado = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            quantidade_total = self.quantidade_produzida * self.receita.quantidade_produzida
            for item in self.receita.itens.all():
                ingrediente = item.ingrediente
                quantidade_a_debitar = item.quantidade * quantidade_total
                if ingrediente.quantidade_estoque < Decimal(str(quantidade_a_debitar)):
                    raise ValueError(f"Estoque insuficiente para {ingrediente.nome}. Disponível: {ingrediente.quantidade_estoque} {ingrediente.unidade_medida}, Necessário: {quantidade_a_debitar} {ingrediente.unidade_medida}")
                ingrediente.quantidade_estoque -= Decimal(str(quantidade_a_debitar))
                ingrediente.save()
            super().save(*args, **kwargs)
            if self.produto_gerado:
                self.produto_gerado.quantidade_estoque += quantidade_total
                self.produto_gerado.save()
            else:
                produto, created = Produto.objects.get_or_create(
                    nome=self.receita.nome,
                    defaults={
                        'quantidade_estoque': quantidade_total,
                        'preco_venda': self.receita.preco_por_unidade
                    }
                )
                self.produto_gerado = produto
                super().save(update_fields=['produto_gerado'])

    def __str__(self):
        return f"Fornada de {self.receita.nome} ({self.quantidade_produzida} execuções = {self.quantidade_produzida * self.receita.quantidade_produzida} unidades)"

    class Meta:
        verbose_name = "Fornada"
        verbose_name_plural = "Fornadas"