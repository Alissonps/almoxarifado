from django import forms
from .models import Item, Retirada, ItemRetirado
from django.forms import formset_factory

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'descricao', 'quantidade', 'categoria', 'localizacao', 'estoque_minimo']

class RetiradaForm(forms.ModelForm):
    class Meta:
        model = Retirada
        fields = ['observacao']  # O campo 'usuario' não é exibido no formulário

class ItemRetiradoForm(forms.ModelForm):
    class Meta:
        model = ItemRetirado
        fields = ['item', 'quantidade']

# Cria um formset para os itens retirados
ItemRetiradoFormSet = formset_factory(ItemRetiradoForm, extra=1)