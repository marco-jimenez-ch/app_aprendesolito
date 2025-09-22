from django.shortcuts import render

# Create your views here.
import json
from pathlib import Path
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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

def carrito(request):
    return render(request, "carrito.html")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
        messages.error(request, "Credenciales inválidas.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

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
    return not user.is_staff

def es_instructor(user: User):
    return user.is_staff

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
