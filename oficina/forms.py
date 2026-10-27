from django import forms
from django.forms import inlineformset_factory

from .models import ConfiguracaoCustos, Material, Servico

DATA = forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ["cliente", "veiculo", "tipo", "urgencia", "lanternagem", "preparacao", "pintura",
                  "prazo", "preco", "status", "inicio", "fim", "materiais_reais",
                  "erro", "erro_etapa", "erro_custo", "erro_obs"]
        widgets = {"inicio": DATA, "fim": DATA}

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
