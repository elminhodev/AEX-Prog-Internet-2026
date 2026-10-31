from django.test import TestCase

from .forms import ServicoForm


class PlacaTests(TestCase):
    def veiculo(self, texto):
        form = ServicoForm({"veiculo": texto, "tipo": "outro", "urgencia": "normal",
                            "status": "execucao", "prazo": 1, "preco": "100",
                            "inicio": "2026-10-31"})
        form.is_valid()
        return form

    def test_placas_validas(self):
        for texto, esperado in [("Gol, ABC-1234", "GOL, ABC-1234"),
                                ("gol abc1234", "GOL ABC-1234"),
                                ("Onix BRA2E19", "ONIX BRA2E19"),
                                ("Onix bra-2e19", "ONIX BRA2E19")]:
            f = self.veiculo(texto)
            self.assertNotIn("veiculo", f.errors, texto)
            self.assertEqual(f.cleaned_data["veiculo"], esperado)

    def test_placas_invalidas(self):
        for texto in ["XXX-XXXX", "XXX-XXXX-", "Gol", "AB-1234", "ABCD-1234",
                      "ABC-12345", "123-ABCD", "ABC-12"]:
            self.assertIn("veiculo", self.veiculo(texto).errors, texto)