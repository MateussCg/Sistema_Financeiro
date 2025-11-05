from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from ingredientes.models import Ingrediente

class Receita(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    quantidade_produzida = models.PositiveIntegerField(default=1, help_text="Quantidade de produtos gerados por receita")
    preco_por_unidade = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], help_text="Preço de venda por unidade do produto gerado")
    modo_preparo = models.TextField(blank=True, help_text="Modo de preparo, um passo por linha.")
    foto = models.ImageField(upload_to='receitas/', blank=True, null=True)
    profissional = models.CharField(max_length=100, blank=True, null=True)
    rendimento = models.IntegerField(default=20, help_text="Número de porções.")
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    custo_por_porcao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"

class ItemReceita(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='itens')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.FloatField(validators=[MinValueValidator(0)])
    quantidade_bruta = models.FloatField(null=True, blank=True)
    quantidade_liquida = models.FloatField(null=True, blank=True)
    fator_correcao = models.DecimalField(max_digits=5, decimal_places=3, default=1.000)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.quantidade} {self.ingrediente.unidade_medida} de {self.ingrediente.nome} para {self.receita.nome}"

    def save(self, *args, **kwargs):
        if not self.ingrediente_id:
            raise ValueError("O campo 'ingrediente' é obrigatório.")
        if not self.valor_unitario and self.ingrediente:
            self.valor_unitario = self.ingrediente.preco_unitario
        if self.quantidade_bruta and self.fator_correcao:
            self.quantidade_liquida = self.quantidade_bruta * self.fator_correcao
        elif self.quantidade:
            self.quantidade_liquida = self.quantidade
        if self.quantidade_liquida and self.valor_unitario:
            self.custo = self.quantidade_liquida * self.valor_unitario
        super().save(*args, **kwargs)

    def clean(self):
        if not self.ingrediente_id:
            raise ValidationError("O campo 'ingrediente' é obrigatório.")