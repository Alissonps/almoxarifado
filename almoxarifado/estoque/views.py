from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import F
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.forms import formset_factory
from .forms import RetiradaForm, ItemRetiradoForm, ItemForm
from .models import Retirada, ItemRetirado, Item
import pandas as pd

@login_required
def lista_itens(request):
    query = request.GET.get('q')
    if query:
        itens = Item.objects.filter(nome__icontains=query) | Item.objects.filter(categoria__icontains=query)
    else:
        itens = Item.objects.all()

    # Configura a paginação
    paginator = Paginator(itens, 10)  # Exibe 10 itens por página
    page_number = request.GET.get('page')  # Obtém o número da página da URL
    page_obj = paginator.get_page(page_number)  # Obtém os itens da página atual

    return render(request, 'estoque/lista_itens.html', {'page_obj': page_obj, 'query': query})

@login_required
def pagina_inicial(request):
    # Itens com baixo estoque
    itens_baixo_estoque = Item.objects.filter(quantidade__lt=F('estoque_minimo'))
    
    # Últimos itens adicionados (últimos 5 itens)
    ultimos_itens = Item.objects.order_by('-id')[:5]
    
    return render(request, 'estoque/pagina_inicial.html', {
        'itens_baixo_estoque': itens_baixo_estoque,
        'ultimos_itens': ultimos_itens,
    })

@login_required
def adicionar_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_itens')  # Redireciona para a lista de itens após salvar
    else:
        form = ItemForm()
    return render(request, 'estoque/adicionar_item.html', {'form': form})

@login_required
def editar_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('lista_itens')
    else:
        form = ItemForm(instance=item)
    return render(request, 'estoque/editar_item.html', {'form': form})

@login_required
def excluir_item(request, id):
    item = get_object_or_404(Item, id=id)
    if ItemRetirado.objects.filter(item=item).exists():
        return HttpResponse("Este item possui retiradas associadas e não pode ser excluído.", status=403)
    item.delete()
    return redirect('lista_itens')

@login_required
def exportar_itens(request, formato):
    # Recupera todos os itens do banco de dados
    itens = Item.objects.all()
    
    # Cria um DataFrame do pandas com os dados dos itens
    dados = {
        'Nome': [item.nome for item in itens],
        'Descrição': [item.descricao for item in itens],
        'Quantidade': [item.quantidade for item in itens],
        'Categoria': [item.categoria for item in itens],
        'Localização': [item.localizacao for item in itens],
        'Estoque Mínimo': [item.estoque_minimo for item in itens],
    }
    df = pd.DataFrame(dados)
    
    # Exporta para o formato solicitado
    if formato == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="itens_almoxarifado.csv"'
        df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
    elif formato == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="itens_almoxarifado.xlsx"'
        df.to_excel(response, index=False, engine='openpyxl')
    else:
        return HttpResponse("Formato não suportado.", status=400)
    
    return response


def logout_view(request):
    logout(request)  # Realiza o logout
    return render(request, 'estoque/logout.html')  # Renderiza a página personalizada de logout

from django.shortcuts import render, redirect
from django.forms import formset_factory
from .forms import RetiradaForm, ItemRetiradoForm, ItemRetiradoFormSet
from .models import Retirada, ItemRetirado

def criar_retirada(request):
    ItemRetiradoFormSet = formset_factory(ItemRetiradoForm, extra=1)

    if request.method == 'POST':
        retirada_form = RetiradaForm(request.POST)
        item_retirado_formset = ItemRetiradoFormSet(request.POST)

        if retirada_form.is_valid() and item_retirado_formset.is_valid():
            for form in item_retirado_formset:
                if form.cleaned_data:
                    item = form.cleaned_data['item']
                    quantidade = form.cleaned_data['quantidade']
                    if item.quantidade < quantidade:
                        form.add_error('quantidade', 'Estoque insuficiente.')
                        return render(request, 'estoque/criar_retirada.html', { ... })

            return redirect('lista_retiradas')
    else:
        retirada_form = RetiradaForm()
        item_retirado_formset = ItemRetiradoFormSet()

    return render(request, 'estoque/criar_retirada.html', {
        'retirada_form': retirada_form,
        'item_retirado_formset': item_retirado_formset,
    })

def lista_retiradas(request):
    retiradas = Retirada.objects.all()
    return render(request, 'estoque/lista_retiradas.html', {'retiradas': retiradas})

