from decimal import Decimal

from django.db import models
from django.utils import timezone

D0 = Decimal("0")
MULT_URGENCIA = {"normal": Decimal("1"), "alta": Decimal("1.5"), "urgente": Decimal("2.5")}


class ConfiguracaoCustos(models.Model):
    """Custos fixos da funilaria (existe um único registro)."""
    aluguel = models.DecimalField("Aluguel", max_digits=10, decimal_places=2, default=0)
    energia = models.DecimalField("Energia", max_digits=10, decimal_places=2, default=0)
    agua = models.DecimalField("Água", max_digits=10, decimal_places=2, default=0)
    salarios = models.DecimalField("Salários e encargos", max_digits=10, decimal_places=2, default=0)
    outros = models.DecimalField("Outros custos", max_digits=10, decimal_places=2, default=0)
    dias_uteis = models.PositiveIntegerField("Dias úteis no mês", default=22)
    vagas = models.PositiveIntegerField("Vagas do pátio", default=8)
    margem_padrao = models.DecimalField("Margem de lucro padrão (%)", max_digits=6, decimal_places=2, default=100)

    class Meta:
        verbose_name = "configuração de custos"
        verbose_name_plural = "configuração de custos"

    @classmethod
    def atual(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def total_mensal(self):
        return self.aluguel + self.energia + self.agua + self.salarios + self.outros

    @property
    def custo_dia(self):
        """Custo de manter um carro por um dia no pátio."""
        dias_vagas = self.dias_uteis * self.vagas
        return self.total_mensal / dias_vagas if dias_vagas else D0


class Funcionario(models.Model):
    nome = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Servico(models.Model):
    TIPOS = [
        ("para-choque", "Para-choque"), ("retoque", "Retoque e polimento"),
        ("lanternagem", "Lanternagem"), ("pintura-parcial", "Pintura parcial"),
        ("pintura-completa", "Pintura completa"), ("outro", "Outro"),
    ]
    URGENCIAS = [("normal", "Normal"), ("alta", "Alta"), ("urgente", "Urgente")]
    STATUS = [("execucao", "Em execução"), ("concluido", "Concluído")]
    ETAPAS = [("lanternagem", "Lanternagem"), ("preparacao", "Preparação"), ("pintura", "Pintura")]

    cliente = models.CharField(max_length=120, blank=True)
    veiculo = models.CharField("Veículo e placa", max_length=120, blank=True)
    tipo = models.CharField("Tipo de serviço", max_length=20, choices=TIPOS)
    urgencia = models.CharField("Urgência", max_length=10, choices=URGENCIAS, default="normal")
    status = models.CharField(max_length=10, choices=STATUS, default="execucao")
    prazo = models.PositiveIntegerField("Prazo (dias)", default=1)
    preco = models.DecimalField("Valor total (R$)", max_digits=10, decimal_places=2)
    inicio = models.DateField("Início", default=timezone.localdate)
    fim = models.DateField("Conclusão", null=True, blank=True)
    fixado = models.BooleanField("Fixado no topo da fila", default=False)

    lanternagem = models.ForeignKey(Funcionario, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="+", verbose_name="Lanternagem")
    preparacao = models.ForeignKey(Funcionario, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="+", verbose_name="Preparação")
    pintura = models.ForeignKey(Funcionario, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="+", verbose_name="Pintura")

    materiais_reais = models.DecimalField("Materiais reais (R$)", max_digits=10, decimal_places=2,
                                          null=True, blank=True)
    erro = models.BooleanField("Deu errado (retrabalho ou prejuízo)", default=False)
    erro_etapa = models.CharField("Etapa do erro", max_length=12, choices=ETAPAS, blank=True)
    erro_custo = models.DecimalField("Custo do erro (R$)", max_digits=10, decimal_places=2, default=0)
    erro_obs = models.CharField("O que aconteceu", max_length=200, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.veiculo or 'sem veículo'}"

    def save(self, *args, **kwargs):
        if self.status == "concluido" and not self.fim:
            self.fim = timezone.localdate()
        elif self.status == "execucao":
            self.fim = None
        super().save(*args, **kwargs)

    # ---- cálculos (vêm do protótipo HTML) ----
    @property
    def custo_dia(self):
        if not hasattr(self, "_custo_dia"):
            self._custo_dia = ConfiguracaoCustos.atual().custo_dia
        return self._custo_dia

    @property
    def custo_materiais(self):
        return sum((m.preco for m in self.materiais.all()), D0)

    @property
    def custo_previsto(self):
        return self.custo_materiais + self.custo_dia * self.prazo

    @property
    def lucro_previsto(self):
        return self.preco - self.custo_previsto

    @property
    def lucro_dia(self):
        return self.lucro_previsto / max(1, self.prazo)

    @property
    def score(self):
        """Prioridade na fila: lucro por dia de pátio x peso da urgência."""
        return self.lucro_dia * MULT_URGENCIA[self.urgencia]

    @property
    def dias(self):
        fim = self.fim or timezone.localdate()
        return max(1, (fim - self.inicio).days)

    @property
    def atraso(self):
        return max(0, self.dias - self.prazo)

    @property
    def custo_atraso(self):
        return self.atraso * self.custo_dia

    @property
    def lucro_real(self):
        mat = self.materiais_reais if self.materiais_reais is not None else self.custo_materiais
        custo = mat + self.custo_dia * self.dias + (self.erro_custo if self.erro else D0)
        return self.preco - custo

    @property
    def responsavel_erro(self):
        return getattr(self, self.erro_etapa) if self.erro and self.erro_etapa else None


class Material(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name="materiais")
    nome = models.CharField(max_length=100, blank=True)
    preco = models.DecimalField("Preço (R$)", max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome or "Material"
