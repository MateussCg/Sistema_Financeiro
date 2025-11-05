from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    cpf = models.CharField(
        max_length=14,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF deve estar no formato 000.000.000-00')]
    )
    email = models.EmailField(unique=True)
    numero = models.CharField(max_length=15)
    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    numero_endereco = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    intolerancias = models.JSONField(default=list)
    preferencias_alimentares = models.TextField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    ultimo_contato = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome