from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView, DetailView
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

def menu_cbv(request):
    return render(request,'CBV/menu.html')

# Crear nuevo elemento
class autor_created(CreateView):
    template_name = 'CBV/agregar_autor.html'
    form_class = AutorForm
    queryset = Autor.objects.all()
    # para hacer override al reverse en el modelo
    # success_url = 'menu2'
    def form_valid(self, form):
        print(form.cleaned_data)
        return super(autor_created,self).form_valid(form)

    # def get_success_url(self):
        # return 'menu'

# Listar elementos
class autores_list(ListView):
    model = Autor
    template_name = 'CBV/autores_lista.html'
# detalles del elemento
class autores_detalles(DetailView):
    template_name = 'CBV/autor_detalles.html'
    # queryset = Autor.objects.all()

    # Override
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Autor,id = id_)

# Editar elementos
class autor_update(UpdateView):
    template_name = 'CBV/agregar_autor.html'
    form_class = AutorForm
    # para hacer override al reverse en el modelo
    # success_url = 'menu2'
    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Autor,id = id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(autor_update,self).form_valid(form)

class autor_delete(DeleteView):
    template_name = 'CBV/autores_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Autor,id = id_)
    '''
    En el CBV delete es encesario un succes url porque el objeto sera borrado, y el abusolute url del modelo no entrara porque no encontrara el objeto borrado
    '''
    def get_success_url(self):
        return reverse('ver_autores2')
# --------------------------------------------------------------------------------------------
# -------------------------- RAW CLASS BASED VIEWS -------------------------------------------
# --------------------------------------------------------------------------------------------

class couser_object_mixie(object):
    Model = Autor
    lookup = 'pk'
    def get_object(self):
        id = self.kwargs.get(self.lookup)
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model,id=id)
        return obj
class course_detail_autor(couser_object_mixie,View):
    template_name = 'CBV/autor_detalles.html'
    def get (self, request, id=None, *args, **kwargs):
        id = self.kwargs.get('pk')
        context = {'object':self.get_object()}
        return render(request, self.template_name, context)

class course_list_autor(View):
    template_name = "CBV/autores_lista.html"
    queryset = Autor.objects.all()
    print(queryset)
    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list':self.get_queryset()}
        return render(request, self.template_name, context)

class mylistview(course_list_autor):
    queryset = Autor.objects.filter(id=1)


class course_create_autor(View):
    template_name = 'CBV/agregar_autor.html'
    def get (self, request, *args, **kwargs):
        form = AutorForm()
        context = {"form":form}
        return render(request, self.template_name, context)
    def post (self, request, *args, **kwargs):
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            form = AutorForm()
        context = {"form":form}
        return render(request, self.template_name, context)

class course_update_autor(couser_object_mixie,View):
    template_name = "CBV/editar_autor.html"
    
    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AutorForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name,context)
    
    def post (self, request, id=None, * args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AutorForm(request.POST,instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

class course_delete_autor(couser_object_mixie,View):
    template_name = "CBV/autores_delete.html"
    
    def get (self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)
    
    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('course_list_autor')
        return render(request, self.template_name, context)


'''
    mixin es una herencia de elementos que pueden ser llamados desde los argumentos de la clase y la view
    ejem:
    el id es consultado es creado en el mixin y es pasago a la clase princiapl donde es usada.
'''
class autor_form_mixin(object):
    model = Autor
    def getobject(self):
        id = self.kwargs.get('pk')
        obj = None
        initial = None
        form = None
        # si dentro de la url hay una pk significa que hay un id para editar
        if id is not None:
            obj = get_object_or_404(self.model,id = id)
            initial = {
                'nombre': obj.nombre,
                'apellidos': obj.apellidos,
                'email': obj.email}
            form = self.form_class(initial=initial,instance=obj)
        else:
            form = self.form_class()
        return form

class autor_form(autor_form_mixin,View):
    template_name = 'CBV/agregar_autor.html'
    form_class = AutorForm

    # Primera vuelta, cuando se recupera por primera vez la vista
    # get es el proceso default de la clase y se ejecutara.
    def get(self, request, *args, **kwargs):
        form = self.getobject()
        return render(request, self.template_name, {'form': form})
    # cuando se hace una accion post.
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # <process form cleaned data>
            return HttpResponseRedirect('/menu2/')

        return render(request, self.template_name, {'form': form})