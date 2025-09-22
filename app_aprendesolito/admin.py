from django.contrib import admin
from .models import Curso

# Register your models here.
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("codigo","nombre","cupos","activo","creado_por","creado_en")
    search_fields = ("codigo","nombre")
    list_filter = ("activo",)
    