import re

from django import forms
from django.forms import inlineformset_factory

from .models import ConfiguracaoCustos, Material, Servico

DATA = forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")

# Placa antiga (ABC-1234 ou ABC1234) e placa Mercosul (ABC1D23).
PLACA_RE = re.compile(r"(?<![A-Z0-9])([A-Z]{3})-?(\d{4}|\d[A-Z]\d{2})(?![A-Z0-9])")


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ["cliente", "veiculo", "tipo", "urgencia", "lanternagem", "preparacao", "pintura",
                  "prazo", "preco", "status", "inicio", "fim", "materiais_reais",
                  "erro", "erro_etapa", "erro_custo", "erro_obs"]
        widgets = {
            "inicio": DATA,
            "fim": DATA,
            "veiculo": forms.TextInput(attrs={"placeholder": "Ex.: Gol, ABC-1234 ou Onix, BRA2E19"}),
        }

    def clean_veiculo(self):
        texto = self.cleaned_data["veiculo"].strip().upper()
        if not texto:
            return texto
        achada = PLACA_RE.search(texto)
        if not achada:
            raise forms.ValidationError(
                "Informe uma placa válida (ex.: ABC-1234 ou ABC1D23).")
        letras, resto = achada.groups()
        # padroniza: placa antiga com hífen, Mercosul sem hífen
        placa = f"{letras}-{resto}" if resto.isdigit() else f"{letras}{resto}"
        return texto[:achada.start()] + placa + texto[achada.end():]

    def clean_prazo(self):
        prazo = self.cleaned_data["prazo"]
        if prazo < 1:
            raise forms.ValidationError("O prazo deve ser de pelo menos 1 dia.")
        return prazo

    def clean(self):
        dados = super().clean()
        ini, fim = dados.get("inicio"), dados.get("fim")
        if ini and fim and fim < ini:
            self.add_error("fim", "A conclusão não pode ser anterior ao início.")
        return dados


MaterialFormSet = inlineformset_factory(Servico, Material, fields=("nome", "preco"), extra=1, can_delete=True)


class CustosForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoCustos
        fields = "__all__"