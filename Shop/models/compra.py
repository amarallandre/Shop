from django.db import models
from django.utils import timezone
from .produto import Produto



class Compra(models.Model):
    criada_em = models.DateTimeField(default=timezone.now)
    produtos = models.ManyToManyField('Produto', through='CompraProduto')

class CompraProduto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    nome_produto = models.CharField(max_length=255)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)