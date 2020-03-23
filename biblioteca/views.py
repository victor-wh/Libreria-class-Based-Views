from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse
from biblioteca.forms import FormularioAutor
from biblioteca.forms import AutorForm
from .models import *
from biblioteca.forms import EditorForm
from biblioteca.forms import LibroForm
import random
from notifications.signals import notify
from biblioteca.models import Autor
from django.db.models.signals import post_save
from django.views import View


def my_handler(request):
    notify.send(sender=request.user, recipient=request.user, verb='you loaded the page')
    print(request.user)
    return render(request, 'test_live.html', {
        'unread_count': request.user.notifications.unread().count(),
        'notifications': request.user.notifications.all(),
        'url_regreso': reverse('make_notification')
    })

def make_notification(request):

    the_notification = random.choice([
        'reticulating splines',
        'cleaning the car',
        'jumping the shark',
        'testing the app',
        'attaching the plumbus',
    ])

    notify.send(sender=request.user, recipient=request.user,
                verb='you asked for a notification - you are ' + the_notification)
# Create your views here.
def formulario_buscar(request):
    return render(request,'formulario_buscar.html')
def buscar(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Por favor introduce un termino de busqueda.')
        elif len(q) > 20:
            errors.append('Por favor introduce un termino de busqueda menor a 20 caracteres.')
        else:
            libros = Libro.objects.filter(titulo__icontains = q)
            return render(request,'resultados.html',{'libros':libros,'query':q})
    return render(request,'formulario_buscar.html',{'error':errors})
#Editar libros
def menu(request):
    return render(request,'menu.html')

def autores(request):
    autores = Autor.objects.all()
    return render(request,'resultados_autores.html',{'autores':autores})

def autor_view (request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/autores/')
    else:
        form = AutorForm()
    return render(request,'agregar_autor.html',{'form':form})

def autor_edit(request,id_autor):
    autor = Autor.objects.get(id = id_autor)
    if request.method == 'GET':
        form = AutorForm(instance=autor)
    else:
        form = AutorForm(request.POST,instance=autor)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/autores/')
    return render(request,'editar_autor.html',{'form':form})

def autor_delete(request,id_autor):
    autor = Autor.objects.get(id = id_autor)
    if request.method == 'POST':
        autor.delete()
        return HttpResponseRedirect('/autores/')
    return render(request, 'autor_delete.html',{'autor':autor})

# Version recortada de procesos de consulta
# Class based views
class AutorList(ListView):
    model = Autor
    template_name = 'resultados_autores.html'

class AutorCreate(CreateView):
    model = Autor
    form_class = AutorForm
    template_name = 'agregar_autor.html'
    success_url = reverse_lazy('autores')

class AutorUpdate(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'editar_autor.html'
    success_url = reverse_lazy('autores')

class AutorDelete(DeleteView):
    model = Autor
    template_name = 'autor_delete.html'
    success_url = reverse_lazy('autores')
#Editor
class EditorList(ListView):
    model = Editor
    template_name = 'editor_list.html'

class EditorCreate(CreateView):
    model = Editor
    form_class = EditorForm
    template_name = 'editor_form.html'
    success_url = reverse_lazy('editores')

class EditorUpdate(UpdateView):
    model = Editor
    form_class = EditorForm
    template_name = 'editor_edit.html'
    success_url=reverse_lazy('editores')

class EditorDelete(DeleteView):
    model = Editor
    template_name = 'editor_delete.html'
    success_url = reverse_lazy('editores')
#Libros
class LibroList(ListView):
    model = Libro
    template_name = 'libro_list.html'
class LibroCreate(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'
    success_url = reverse_lazy('libros')
class LibroUpdate(UpdateView):
    model = Libro
    form_class=LibroForm
    template_name = 'libro_edit.html'
    success_url=reverse_lazy('libros')
class LibroDelete(DeleteView):
    model = Libro
    form_class=LibroForm
    template_name = 'libro_delete.html'
    success_url=reverse_lazy('libros')

# Cursos de Class based views

class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)

class MorningGreetingView(GreetingView):
    greeting = "Morning to ya"

class MyFormView(View):
    form_class = AutorForm
    initial = {
        'nombre': 'nombre'}
    template_name = ''

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return HttpResponseRedirect('/menu/')

        return render(request, self.template_name, {'form': form})