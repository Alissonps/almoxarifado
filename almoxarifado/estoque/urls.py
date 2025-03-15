from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),  # Página inicial do app estoque
    path('itens/', views.lista_itens, name='lista_itens'),  # Lista de itens
    path('adicionar/', views.adicionar_item, name='adicionar_item'),
    path('editar/<int:id>/', views.editar_item, name='editar_item'),
    path('excluir/<int:id>/', views.excluir_item, name='excluir_item'),
    path('exportar/<str:formato>/', views.exportar_itens, name='exportar_itens'),
    path('retiradas/', views.lista_retiradas, name='lista_retiradas'),
    path('retiradas/nova/', views.criar_retirada, name='criar_retirada'),
    
]