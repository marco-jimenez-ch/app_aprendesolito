from pathlib import Path
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Curso

BASE_DIR = Path(__file__).resolve().parent.parent

def _load_cursos():
    data_path = BASE_DIR / "data" / "cursos.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def index(request):
    return render(request, "index.html")

def cursos(request):
    cursos = _load_cursos()
    return render(request, "cursos.html", {"cursos": cursos})

def detalle_curso(request, curso_id: int):
    cursos = _load_cursos()
    curso = next((c for c in cursos if c.get("id") == curso_id), None)
    return render(request, "detalle-curso.html", {"curso": curso})

@login_required
def carrito(request):
    return render(request, "carrito.html")

def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url or "index")
        messages.error(request, "Credenciales inválidas.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form, "next": next_url})

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")

def registro_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("perfil")
        messages.error(request, "Error al registrar usuario.")
    else:
        form = UserCreationForm()
    return render(request, "registro.html", {"form": form})

def recuperar_view(request):
    return render(request, "recuperar.html")

@login_required
def perfil(request):
    return render(request, "perfil.html")

def es_estudiante(user: User):
    return user.is_authenticated and not user.is_staff

def es_instructor(user: User):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(es_estudiante)
def panel_estudiante(request):
    return render(request, "panel-estudiante.html")

@login_required
@user_passes_test(es_instructor)
def panel_instructor(request):
    return render(request, "panel-instructor.html")

def exito(request):
    return render(request, "exito.html")

class SoloStaff(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class CursoList(LoginRequiredMixin, ListView):
    model = Curso
    template_name = "cursos_list.html"
    paginate_by = 10

class CursoDetail(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = "cursos_detail.html"

class CursoCreate(LoginRequiredMixin, SoloStaff, CreateView):
    model = Curso
    fields = ["codigo", "nombre", "descripcion", "cupos", "activo"]
    template_name = "cursos_form.html"
    success_url = reverse_lazy("cursos_list")
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

class CursoUpdate(LoginRequiredMixin, SoloStaff, UpdateView):
    model = Curso
    fields = ["nombre", "descripcion", "cupos", "activo"]
    template_name = "cursos_form.html"
    success_url = reverse_lazy("cursos_list")

class CursoDelete(LoginRequiredMixin, SoloStaff, DeleteView):
    model = Curso
    template_name = "cursos_confirm_delete.html"
    success_url = reverse_lazy("cursos_list")
