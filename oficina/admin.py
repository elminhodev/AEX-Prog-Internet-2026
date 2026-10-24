from django.contrib import admin

from .models import ConfiguracaoCustos, Funcionario, Material, Servico


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 0


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "cliente", "status", "urgencia", "preco")
    inlines = [MaterialInline]


admin.site.register(ConfiguracaoCustos)
admin.site.register(Funcionario)
