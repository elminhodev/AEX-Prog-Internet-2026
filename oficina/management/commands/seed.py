from datetime import timedelta
from decimal import Decimal as D

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from oficina.models import ConfiguracaoCustos, Funcionario, Material, Servico


class Command(BaseCommand):
    help = "Cria usuário de teste (dono / funilaria123) e dados de exemplo."

    def handle(self, *args, **opts):
        if not User.objects.filter(username="dono").exists():
            User.objects.create_superuser("dono", "dono@exemplo.com", "funilaria123")
        cfg = ConfiguracaoCustos.atual()
        cfg.aluguel, cfg.energia, cfg.agua = D(4500), D(1800), D(350)
        cfg.salarios, cfg.outros = D(18000), D(1200)
        cfg.save()
        marcos, rafael, josue = (Funcionario.objects.get_or_create(nome=n)[0]
                                 for n in ("Marcos", "Rafael", "Josué"))
        if Servico.objects.exists():
            self.stdout.write("Já existem serviços; nada a criar.")
            return
        hoje = timezone.localdate()
        dados = [
            ("Carlos Silva", "Gol, ABC-1234", "para-choque", "normal", 2, 900, 0, None, marcos, [("Tinta", 250)]),
            ("Marina Costa", "HB20, DEF-5678", "pintura-completa", "normal", 20, 6500, 26, None, rafael, [("Tinta", 1800)]),
            ("Seguradora Alfa", "Onix, GHI-9012", "lanternagem", "alta", 8, 3200, 3, None, josue, [("Massa e peças", 900)]),
            ("Ana Lima", "Corolla, MNO-7890", "pintura-parcial", "normal", 6, 2600, 20, 10, rafael, [("Tinta", 700)]),
        ]
        for cli, vei, tipo, urg, prazo, preco, ini, fim, resp, mats in dados:
            s = Servico.objects.create(
                cliente=cli, veiculo=vei, tipo=tipo, urgencia=urg, prazo=prazo, preco=preco,
                inicio=hoje - timedelta(days=ini),
                status="concluido" if fim is not None else "execucao",
                fim=hoje - timedelta(days=fim) if fim is not None else None,
                lanternagem=marcos, preparacao=josue, pintura=resp)
            for nome, p in mats:
                Material.objects.create(servico=s, nome=nome, preco=p)
        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados. Login: dono / funilaria123"))
