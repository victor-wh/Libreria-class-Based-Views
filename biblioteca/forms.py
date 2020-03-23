from django import forms
from biblioteca.models import Autor
from biblioteca.models import Editor
from biblioteca.models import Libro

class FormularioAutor(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellidos = forms.CharField()
    email = forms.EmailField(required=False)

class AutorForm(forms.ModelForm):

    class Meta:
        model = Autor

        fields = [
            'nombre',
            'apellidos',
            'email',
        ]
        labels ={
            'nombre':'Nombre',
            'apellidos':'Apellidos',
            'email':'Email',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
        }
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre.lower() == 'abc':
            raise forms.ValidationError("This is not a valid nombre")
        return nombre
class EditorForm(forms.ModelForm):

    class Meta:
        model = Editor

        fields = [
            'nombre',
            'domicilio',
            'ciudad',
            'estado',
            'pais',
            'website',
        ]

        labels = {
            'nombre':'Nombre',
            'domicilio':'Domicilio',
            'ciudad':'Ciudad',
            'estado':'Estado',
            'pais':'Pais',
            'website':'Website',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'domicilio':forms.TextInput(attrs={'class':'form-control'}),
            'ciudad':forms.TextInput(attrs={'class':'form-control'}),
            'estado':forms.TextInput(attrs={'class':'form-control'}),
            'pais':forms.TextInput(attrs={'class':'form-control'}),
            'website':forms.TextInput(attrs={'class':'form-control'}),
        }
        
class LibroForm(forms.ModelForm):

    class Meta:
        model = Libro

        fields = [
            'titulo',
            'autores',
            'editor',
            'fecha_publicacion',
            'portada',
        ]
        labels = {
            'titulo':'Titulo',
            'autores':'Autores',
            'editor':'Editor',
            'fecha_publicacion':'Fecha de publicacion',
            'portada':'Portada',
        }
        widgets = {
            'titulo':forms.TextInput(attrs={'class':'form-control'}),
            'autores':forms.CheckboxSelectMultiple(),
            'editor':forms.Select(attrs={'class':'form-control'}),
            'fecha_publicacion':forms.DateInput(format=('%d/%m/%Y'),attrs={'class':'form-control'}),
        }