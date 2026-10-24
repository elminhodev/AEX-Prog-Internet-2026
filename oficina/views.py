from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView

from .forms import CustosForm, MaterialFormSet, ServicoForm
from .models import ConfiguracaoCustos, Funcionario, Servico

D0 = Decimal("0")
ETAPAS = ("lanternagem", "preparacao", "pintura")


@login_required
def fila(request):
    cfg = ConfiguracaoCustos.atual()
    servicos = list(Servico.objects.filter(status="execucao")
                    .select_related(*ETAPAS).prefetch_related("materiais"))
    servicos.sort(key=lambda s: (not s.fixado, -s.score))
    return render(request, "oficina/fila.html", {
        "servicos": servicos, "cfg": cfg,
        "perdido_atrasos": sum((s.custo_atraso for s in servicos), D0),
    })


@login_required
def servico_form(request, pk=None):
    obj = get_object_or_404(Servico, pk=pk) if pk else None
    form = ServicoForm(request.POST or None, instance=obj)
    formset = MaterialFormSet(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        servico = form.save()
        formset.instance = servico
        formset.save()
        messages.success(request, "Serviço salvo.")
        return redirect("fila")
    cfg = ConfiguracaoCustos.atual()
    return render(request, "oficina/servico_form.html", {
        "form": form, "formset": formset, "obj": obj,
        "custo_dia": f"{cfg.custo_dia:.2f}", "margem": f"{cfg.margem_padrao:.2f}",
    })


class ServicoExcluir(LoginRequiredMixin, DeleteView):
    model = Servico
    template_name = "oficina/servico_confirm_delete.html"
    success_url = reverse_lazy("fila")


@login_required
@require_POST
def concluir(request, pk):
    s = get_object_or_404(Servico, pk=pk)
    s.status = "concluido"
    s.save()
    messages.success(request, "Serviço concluído.")
    return redirect("fila")


@login_required
@require_POST
def fixar(request, pk):
    s = get_object_or_404(Servico, pk=pk)
    s.fixado = not s.fixado
    s.save()
    return redirect("fila")


@login_required
def custos(request):
    cfg = ConfiguracaoCustos.atual()
    form = CustosForm(request.POST or None, instance=cfg)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Custos salvos.")
        return redirect("custos")
    return render(request, "oficina/custos.html", {
        "form": form, "cfg": cfg, "equipe": Funcionario.objects.all()})


@login_required
@require_POST
def equipe_adicionar(request):
    nome = request.POST.get("nome", "").strip()
    if nome:
        Funcionario.objects.get_or_create(nome=nome)
    return redirect("custos")


@login_required
@require_POST
def equipe_remover(request, pk):
    get_object_or_404(Funcionario, pk=pk).delete()
    return redirect("custos")


@login_required
def relatorio(request):
    fin = list(Servico.objects.filter(status="concluido")
               .select_related(*ETAPAS).prefetch_related("materiais"))
    faturado = sum((s.preco for s in fin), D0)
    lucro = sum((s.lucro_real for s in fin), D0)
    perdido = sum((s.custo_atraso + (s.erro_custo if s.erro else D0) for s in fin), D0)

    por_func = []
    for f in Funcionario.objects.all():
        total = sum(1 for s in Servico.objects.all() if f.id in
                    {s.lanternagem_id, s.preparacao_id, s.pintura_id})
        erros = [s for s in fin if s.responsavel_erro == f]
        por_func.append({"nome": f.nome, "total": total, "erros": len(erros),
                         "custo": sum((s.erro_custo for s in erros), D0)})
    por_func.sort(key=lambda x: (-x["erros"], -x["custo"]))

    tipos = defaultdict(lambda: {"qtd": 0, "lucro": D0, "dias": 0})
    for s in fin:
        t = tipos[s.get_tipo_display()]
        t["qtd"] += 1
        t["lucro"] += s.lucro_real
        t["dias"] += s.dias
    por_tipo = [{"nome": k, "qtd": v["qtd"], "lucro": v["lucro"],
                 "por_dia": v["lucro"] / max(1, v["dias"])} for k, v in tipos.items()]
    por_tipo.sort(key=lambda x: -x["por_dia"])

    return render(request, "oficina/relatorio.html", {
        "fin": fin, "faturado": faturado, "lucro": lucro, "perdido": perdido,
        "por_func": por_func, "por_tipo": por_tipo})
