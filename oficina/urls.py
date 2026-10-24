from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.fila, name="fila"),
    path("servicos/novo/", views.servico_form, name="servico_novo"),
    path("servicos/<int:pk>/editar/", views.servico_form, name="servico_editar"),
    path("servicos/<int:pk>/excluir/", views.ServicoExcluir.as_view(), name="servico_excluir"),
    path("servicos/<int:pk>/concluir/", views.concluir, name="servico_concluir"),
    path("servicos/<int:pk>/fixar/", views.fixar, name="servico_fixar"),
    path("custos/", views.custos, name="custos"),
    path("equipe/adicionar/", views.equipe_adicionar, name="equipe_adicionar"),
    path("equipe/<int:pk>/remover/", views.equipe_remover, name="equipe_remover"),
    path("relatorio/", views.relatorio, name="relatorio"),
    path("entrar/", LoginView.as_view(), name="login"),
    path("sair/", LogoutView.as_view(), name="logout"),
]
