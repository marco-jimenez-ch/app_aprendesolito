from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cursos/", views.cursos, name="cursos"),
    path("curso/<int:curso_id>/", views.detalle_curso, name="detalle_curso"),
    path("carrito/", views.carrito, name="carrito"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registro/", views.registro_view, name="registro"),
    path("recuperar/", views.recuperar_view, name="recuperar"),
    path("panel-estudiante/", views.panel_estudiante, name="panel_estudiante"),
    path("panel-instructor/", views.panel_instructor, name="panel_instructor"),
    path("perfil/", views.perfil, name="perfil"),
    path("exito/", views.exito, name="exito"),
]
