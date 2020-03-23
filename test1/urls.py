"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from test1.views import hola,fecha_actual,horas_adelante,mostrar_navegador,atributos_meta
#from django.contrib import admin
from django.conf.urls import url,include
from django.contrib import admin
from biblioteca import views

from biblioteca.views import AutorList,AutorCreate,AutorUpdate,AutorDelete,EditorList,\
EditorCreate,EditorUpdate,EditorDelete,LibroList,LibroCreate,LibroUpdate,LibroDelete,GreetingView,MorningGreetingView,MyFormView

from biblioteca.class_based_views import (
    menu_cbv,
    autores_list, 
    autor_form, 
    autores_detalles, 
    autor_created,
    autor_update,
    autor_delete,
    course_detail_autor,
    course_list_autor,
    mylistview,
    course_create_autor,
    course_update_autor,
    course_delete_autor,
    )
from contactos.views import contactos
from contactos.views import gracias
import notifications.urls



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hola/$',hola),
    url(r'^fecha/$',fecha_actual),
    url(r'^fecha/mas/(\d{1,2})/$',horas_adelante),
    url(r'^navegador/$',mostrar_navegador),
    url(r'^atributos/$',atributos_meta),
    url(r'^formulario-buscar/$',views.formulario_buscar),
    url(r'^buscar/$',views.buscar),
    #URLS libros
    url(r'^menu/$',views.menu,name="menu"),
    url(r'^agregar-autor/$',views.autor_view,name = 'autor_view'),
    url(r'^editar-autor/(?P<id_autor>\d+)/$',views.autor_edit, name='autor_edit'),
    url(r'^autores/$',views.autores,name = 'autores'),
    url(r'^eliminar-autor/(?P<id_autor>\d+)/$',views.autor_delete,name='autor_delete'),
    url(r'^contactos/$',contactos),
    url(r'^contactos/gracias/$',gracias),
    #URLS Editores
    url(r'^editores/$',EditorList.as_view(),name = 'editores'),
    url(r'^agregar-editor/$',EditorCreate.as_view(), name='editor_view'),
    url(r'^editar-editor/(?P<pk>\d+)$',EditorUpdate.as_view(),name='editor_edit'),
    url(r'^eliminar-editor/(?P<pk>\d+)$',EditorDelete.as_view(),name='editor_delete'),
    #URLS Libros
    url(r'^libros/$',LibroList.as_view(),name='libros'),
    url(r'^agregar-libros/$',LibroCreate.as_view(),name='libro_view'),
    url(r'^editar-libros/(?P<pk>\d+)$',LibroUpdate.as_view(),name='libro_edit'),
    url(r'^eliminar-libros/(?P<pk>\d+)$',LibroDelete.as_view(),name='libro_delete'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^noti/$',views.my_handler, name = 'my_handler'),
    url(r'^makenoti/$',views.make_notification, name='make_notification'),
    # ------------------------------------------------------------------------------------
    # Vistas basadas en clases
    url(r'^home/$', GreetingView.as_view(greeting="G'day")),
    url(r'^home2/$',MorningGreetingView.as_view()),
    url(r'^myform/$',MyFormView.as_view(template_name = 'agregar_autor.html')),
    # libreria con CBV
    url(r'^menu2/$',menu_cbv, name = "menu2"),
    url(r'^agregar-autor2/$',autor_form.as_view(),name='agregar_autor2'),
    url(r'^editar-autor2/(?P<pk>\d+)$',autor_form.as_view(template_name='CBV/editar_autor.html'),name='editar_autor2'),
    # -----------------------------------------------------------------------------------
    url(r'^ver-autores2/$', autores_list.as_view(),name = 'ver_autores2'),
    url(r'^detalles-autor2/(?P<pk>\d+)$', autores_detalles.as_view(), name='autores_detalles2'),
    url(r'^agregar-autor22/$', autor_created.as_view(),name='agregar_autor22'),
    url(r'^editar-autor22/(?P<pk>\d+)$', autor_update.as_view(), name='autor_update'),
    url(r'^delete-autor22/(?P<pk>\d+)$', autor_delete.as_view(), name='autor_delete'),
    # ---------------------------RAW CBV -------------------------------------------------
    url(r'^course-detail-autor/(?P<pk>\d+)$',course_detail_autor.as_view(), name='course_detail_autor'),
    url(r'^course-list-autor/$',course_list_autor.as_view(), name='course_list_autor'),
    url(r'^mylistview/$',mylistview.as_view(),name="mylistview"),
    url(r'^course-create-autor/$',course_create_autor.as_view(), name="course_create_autor"),
    url(r'^course_update_autor/(?P<pk>\d+)$',course_update_autor.as_view(), name='course_update_autor'),
    url(r'^course_delete_autor/(?P<pk>\d+)$',course_delete_autor.as_view(), name='course_delete_autor'),
]
