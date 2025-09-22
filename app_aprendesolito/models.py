from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Curso(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    cupos = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="cursos_creados")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"