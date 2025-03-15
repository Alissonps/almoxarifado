from django.db import models, transaction
from django.contrib.auth.models import User

# Create your models here.


from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Item")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    quantidade = models.IntegerField(verbose_name="Quantidade em Estoque", default=0)
    categoria = models.CharField(max_length=50, verbose_name="Categoria", blank=True, null=True)
    localizacao = models.CharField(max_length=100, verbose_name="Localização", blank=True, null=True)
    estoque_minimo = models.IntegerField(verbose_name="Estoque Mínimo", default=0)

    def __str__(self):
        return self.nome
    
class Retirada(models.Model):
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data da Retirada")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    def __str__(self):
        return f"Retirada #{self.id} - {self.data.strftime('%d/%m/%Y %H:%M')}"

class ItemRetirado(models.Model):
    retirada = models.ForeignKey(Retirada, on_delete=models.CASCADE, related_name='itens_retirados')
    item = models.ForeignKey('Item', on_delete=models.CASCADE, verbose_name="Item")
    quantidade = models.IntegerField(verbose_name="Quantidade Retirada")

    def __str__(self):
        return f"{self.item.nome} - {self.quantidade} unidades"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.item.quantidade = F('quantidade') - self.quantidade
            self.item.save()
            super().save(*args, **kwargs)